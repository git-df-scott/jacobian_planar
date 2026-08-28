"""night11 numeric net -- polynomial kernel (float64, numpy).

Representation
--------------
A bivariate polynomial of degree <= d is a dense array A of shape (d+1, d+1)
with A[i, j] = coefficient of x^i y^j.  Entries outside the admissible support
are held at exactly 0 by the mask machinery in `supports.py`.

Everything here is measurement plumbing: residuals, energies, gradients.
No claims are made about what the numbers mean.
"""

import numpy as np

# ---------------------------------------------------------------- 2D helpers


def _fftshape(n1, n2):
    """Smallest 5-smooth size >= n for each axis (numpy fft is fast on those)."""
    out = []
    for n in (n1, n2):
        m = 1
        while m < n:
            m *= 2
        # try 3/4 and 7/8 of the power of two if still >= n
        for frac in (0.75, 0.875):
            cand = int(m * frac)
            if cand >= n:
                m = cand
        out.append(m)
    return tuple(out)


def conv2(A, B, shape=None):
    """Linear 2D convolution (polynomial product) via rfft2."""
    n1 = A.shape[0] + B.shape[0] - 1
    n2 = A.shape[1] + B.shape[1] - 1
    s = _fftshape(n1, n2)
    C = np.fft.irfft2(np.fft.rfft2(A, s=s) * np.fft.rfft2(B, s=s), s=s)
    return C[:n1, :n2]


def conv2_direct(A, B):
    """Reference (O(n^4)) polynomial product, used only by control N1."""
    n1 = A.shape[0] + B.shape[0] - 1
    n2 = A.shape[1] + B.shape[1] - 1
    C = np.zeros((n1, n2))
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            a = A[i, j]
            if a != 0.0:
                C[i:i + B.shape[0], j:j + B.shape[1]] += a * B
    return C


def corr2(R, B, out_shape):
    """corr[a,b] = sum_{c,d} R[a+c, b+d] * B[c,d], truncated to out_shape.

    Computed circularly at an FFT size >= R.shape, which is exact here because
    every index a+c that we read is < R.shape (the caller guarantees it).
    """
    s = _fftshape(R.shape[0], R.shape[1])
    C = np.fft.irfft2(np.fft.rfft2(R, s=s) * np.conj(np.fft.rfft2(B, s=s)), s=s)
    return C[:out_shape[0], :out_shape[1]]


def dx(A):
    """d/dx, returned in an array of the same shape (top row zero)."""
    B = np.zeros_like(A)
    n = A.shape[0]
    if n > 1:
        B[:n - 1, :] = A[1:, :] * np.arange(1, n)[:, None]
    return B


def dy(A):
    B = np.zeros_like(A)
    n = A.shape[1]
    if n > 1:
        B[:, :n - 1] = A[:, 1:] * np.arange(1, n)[None, :]
    return B


def dx_adjoint(G):
    """Adjoint of dx: given dE/d(dx A) (same shape as A), give dE/dA."""
    out = np.zeros_like(G)
    n = G.shape[0]
    if n > 1:
        out[1:, :] = G[:n - 1, :] * np.arange(1, n)[:, None]
    return out


def dy_adjoint(G):
    out = np.zeros_like(G)
    n = G.shape[1]
    if n > 1:
        out[:, 1:] = G[:, :n - 1] * np.arange(1, n)[None, :]
    return out


# ------------------------------------------------------------ Keller energy


def _fused(P, Q, want_grad=True):
    Px, Py = dx(P), dy(P)
    Qx, Qy = dx(Q), dy(Q)
    n = P.shape[0] + Q.shape[0] - 1
    s = _fftshape(n, n)
    FPx = np.fft.rfft2(Px, s=s)
    FPy = np.fft.rfft2(Py, s=s)
    FQx = np.fft.rfft2(Qx, s=s)
    FQy = np.fft.rfft2(Qy, s=s)
    FR = FPx * FQy - FPy * FQx - 1.0        # -1.0 in freq == -delta_(0,0)
    R = np.fft.irfft2(FR, s=s)
    E = float(np.sum(R * R))
    if not want_grad:
        return E, R, None, None
    shP, shQ = P.shape, Q.shape
    gPx = 2.0 * np.fft.irfft2(FR * np.conj(FQy), s=s)[:shP[0], :shP[1]]
    gPy = -2.0 * np.fft.irfft2(FR * np.conj(FQx), s=s)[:shP[0], :shP[1]]
    gQy = 2.0 * np.fft.irfft2(FR * np.conj(FPx), s=s)[:shQ[0], :shQ[1]]
    gQx = -2.0 * np.fft.irfft2(FR * np.conj(FPy), s=s)[:shQ[0], :shQ[1]]
    gP = dx_adjoint(gPx) + dy_adjoint(gPy)
    gQ = dx_adjoint(gQx) + dy_adjoint(gQy)
    return E, R, gP, gQ


def keller_residual(P, Q):
    """R = P_x Q_y - P_y Q_x - 1, as a dense coefficient array (padded)."""
    return _fused(P, Q, want_grad=False)[1]


def keller_residual_slow(P, Q):
    """Same, by explicit linear convolutions (reference path for control N1)."""
    R = conv2(dx(P), dy(Q)) - conv2(dy(P), dx(Q))
    R[0, 0] -= 1.0
    return R


def keller_energy_grad(P, Q):
    """E_K = ||R||_2^2 and its gradients w.r.t. the dense arrays P, Q."""
    E, R, gP, gQ = _fused(P, Q)
    return E, gP, gQ, R


# ------------------------------------------------------------- tear proxy


def top_form(A, d):
    """Leading homogeneous part of degree d, as the vector t[i] = A[i, d-i]."""
    idx = np.arange(d + 1)
    return A[idx, d - idx].copy()


def _conv1(a, b):
    return np.convolve(a, b)


def _corr1(g, s):
    """corr[i] = sum_k g[k] s[k-i]; returned with len(g)-len(s)+1 entries."""
    return np.correlate(g, s, mode='valid')


def tear_energy_grad(tP, tQ, tau=1e-2, w_nd=1.0, eps=1e-300):
    """E_T: how far the leading forms are from the (H^2, H^3) shape.

    For a pair of degrees (2m, 3m) the classical shape of a non-proper Keller
    pair has leading forms proportional to H^2 and H^3 for one form H of
    degree m; equivalently  P_top^3  and  Q_top^2  are proportional (both are
    forms of degree 6m).  We measure exactly that proportionality defect:

        A = tP * tP * tP,   B = tQ * tQ      (1D coefficient convolutions)
        E_prop = 1 - <A,B>^2 / (|A|^2 |B|^2)      in [0, 1], scale invariant

    plus a non-degeneracy guard that keeps the leading forms from collapsing:

        E_nd = relu(tau - |tP|^2)^2 + relu(tau - |tQ|^2)^2

    E_T = E_prop + w_nd * E_nd.

    LIMITATION.  This is a proxy on the leading forms only.  It is *not* the
    Jelonek set: it says nothing about the lower-order terms, and the actual
    non-properness locus is cut out by the leading coefficients (in the source
    variable) of Res_y(P-u, Q-v) and Res_x(P-u, Q-v), which are far too heavy
    to form symbolically at degrees (84, 126).  E_prop = 0 is a necessary
    shape condition that the leading forms of the sought pairs satisfy; it is
    in no way sufficient, and a small E_T supports no conclusion whatever.
    """
    A = _conv1(_conv1(tP, tP), tP)
    B = _conv1(tQ, tQ)
    a = float(A @ A)
    b = float(B @ B)
    nP = float(tP @ tP)
    nQ = float(tQ @ tQ)

    gtP = np.zeros_like(tP)
    gtQ = np.zeros_like(tQ)

    if a <= eps or b <= eps:
        E_prop = 1.0
    else:
        # pad the shorter of A, B so the inner product is well defined
        L = max(len(A), len(B))
        Ap = np.zeros(L); Ap[:len(A)] = A
        Bp = np.zeros(L); Bp[:len(B)] = B
        c = float(Ap @ Bp)
        E_prop = 1.0 - c * c / (a * b)
        dA = (-2.0 * c / (a * b)) * Bp + (2.0 * c * c / (a * a * b)) * Ap
        dB = (-2.0 * c / (a * b)) * Ap + (2.0 * c * c / (a * b * b)) * Bp
        S2 = _conv1(tP, tP)
        gtP = 3.0 * _corr1(dA[:len(A)], S2)
        gtQ = 2.0 * _corr1(dB[:len(B)], tQ)

    E_nd = 0.0
    if nP < tau:
        E_nd += (tau - nP) ** 2
        gtP = gtP + w_nd * 2.0 * (tau - nP) * (-2.0 * tP)
    if nQ < tau:
        E_nd += (tau - nQ) ** 2
        gtQ = gtQ + w_nd * 2.0 * (tau - nQ) * (-2.0 * tQ)

    return E_prop + w_nd * E_nd, gtP, gtQ, E_prop, E_nd


def scatter_top(gt, d, shape):
    """Adjoint of top_form."""
    G = np.zeros(shape)
    idx = np.arange(d + 1)
    G[idx, d - idx] = gt
    return G


# ------------------------------------------------------- Sylvester diagnostic


def sylvester_sigma(tP, tQ):
    """Smallest singular values of the Sylvester matrix of the two leading
    forms, dehomogenised in one variable.  Reported only as a post-hoc
    diagnostic (too expensive to sit inside the objective)."""
    p = np.trim_zeros(tP[::-1], 'f')
    q = np.trim_zeros(tQ[::-1], 'f')
    if len(p) < 2 or len(q) < 2:
        return None
    m, n = len(p) - 1, len(q) - 1
    S = np.zeros((m + n, m + n))
    for i in range(n):
        S[i, i:i + m + 1] = p
    for i in range(m):
        S[n + i, i:i + n + 1] = q
    sv = np.linalg.svd(S, compute_uv=False)
    return sv
