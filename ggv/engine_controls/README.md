# Engine acceptance controls, run before the engines were trusted

Small inputs and their exact outputs, kept so the engines' behaviour on this
machine is reproducible rather than asserted.

`ctl_empty.ms`  -> `ctl_empty.out`   the empty ideal <xy-1, x, y>, msolve prints `[-1]:`
`ctl_zd.ms`     -> `ctl_zd.out`      the zero-dimensional ideal <x^2-1, y-2>,
                                     msolve prints a rational parametrization, NOT `[-1]:`
Together these are the pair the campaign tooling contract names as msolve's
verified controls, and they are the same pair GATE-3 re-runs every time.

`toy.sing`   Singular `eliminate()` on <u-x-y, v-x*y, x^2+y^2-1> eliminating x*y,
             which must give `u2-2v-1`.
`toy2.sing`  the same shape with MULTI-CHARACTER variable names (a2, b2, mu0, mu3),
             run to confirm Singular prints full `^`/`*` notation rather than its
             short form for such names -- the eliminant text is fed back into
             Singular by ggv/g23_eliminants.py::normalise, so a short-form
             printing would have silently corrupted every cross-engine comparison.

A finding worth recording: msolve's input format is variables on line 1 and the
characteristic on line 2.  Supplying them in the opposite order does not error --
it returns `[-1]:`, i.e. "no solutions", for a system that plainly has two.  A
transposed header is therefore a silent lie of exactly the kind the campaign's
silent-lie table catalogues, and it is why ggv/g1_gen.py verifies the header and
characteristic lines of every generated file against the builder.
