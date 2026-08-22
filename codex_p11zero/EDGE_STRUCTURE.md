# Coupled-edge structured-family audit

Let `u=xy`.  For diagonal forms one has the exact identity

```text
{y^a f(u), y^b g(u)}
  = y^(a+b) (b f'(u) g(u) - a f(u) g'(u)).
```

Use the exact degenerate anchor

```text
A = x+y = y^-1 u + y,
B = x^2 y + x y^2 + y^3/3 = y^-1 u^2 + y u + y^3/3,
{A,B}=x^2.
```

## One polynomial realizes both required edges

Set

```text
T = y^4 S(u) + lambda x^4 y^7.
```

If `s_4` is the `u^4` coefficient of `S`, then

```text
T^2_top = y^8 S(u)^2,
[T^2]_(x-degree 8) = x^8 y^14 (lambda+s_4 y)^2,

T^3_top = y^12 S(u)^3,
[T^3]_(x-degree 12) = x^12 y^21 (lambda+s_4 y)^3.
```

Thus the same `T` produces the required square/cube slope-one edge and the
required shared square/cube vertical-right edge.

## Exact obstruction to the minimal ansatz

Consider

```text
P=A+T^2,
Q=B+T^3.
```

At `x=0`, `T=s_0 y^4`.  The coefficient of `x^0 y^9` in

```text
{A,T^3}+{T^2,B}
```

is exactly `-8 s_0^2`.  The lower-left top vertex requires `s_0!=0`, so this
cannot vanish in characteristic zero.

Target: the minimal combined-edge ansatz above with `s_0!=0`.

VERDICT: EMPTY

## Exact first-order escape condition

Now write an edge-compatible deformation

```text
P = A + t y^8 F_8(u) + O(t^2),
Q = B + t y^12 G_12(u) + O(t^2),

F_8 = a S_0^2,
G_12 = b S_0^3,
a*b != 0.
```

With weight `w=j-i`, the weight-13 linearized bracket equation is

```text
-G_12' = 0.
```

If no subtop Q line is present at the same order, the weight-11 equation is

```text
F_8' + 12 G_12 + u G_12' = 0.
```

The first equation makes nonzero `G_12` constant, hence `S_0` and `F_8`
constant.  The second then demands `0=-12 G_12`, a contradiction in
characteristic zero.

Target: the pure-high-block first-order subsystem with no same-order subtop Q
line.

VERDICT: EMPTY

Retaining a subtop term `t y^10 G_10(u)` changes weight 11 to

```text
F_8' + 12 G_12 + u G_12' - G_10' = 0.
```

For normalized `F_8=G_12=1`, this forces

```text
G_10 = 12u + constant,
```

so `q_11_1=12` must turn on at first order.  `kernel_order2.py` leaves this
subtop line free and therefore includes the necessary escape direction.

This subsystem analysis does not decide the full all-vertex chart.

VERDICT: NO VERDICT
