# Engine build record

The task named a `BUILD.md`; this repository contains no such file, so msolve
was built exactly as `campaign/moduli_phase2/tools/README.md` prescribes:

    git clone --depth 1 https://github.com/algebraic-solving/msolve.git
    cd msolve && ./autogen.sh && ./configure && make -j4 && make install

with build deps `libgmp-dev libmpfr-dev libflint-dev build-essential libtool
autoconf automake pkg-config`, plus `singular` for the second engine.  Full
transcripts: `msolve_clone.log`, `msolve_build.log`, `apt_packages.log`.

Per that same README, the libtool wrapper `./msolve` in the build tree is NOT
used; `make install` places the real binary at `/usr/local/bin/msolve`.  One
deviation was required and is recorded here: immediately after `make install`
the binary failed with `error while loading shared libraries: libneogb.so.3`,
fixed by running `ldconfig`.

Versions in use:
    msolve   0.10.1 (built from source, /usr/local/bin/msolve)
    Singular 4.3.2 (4330, 64-bit), GMP 6.3.0, NTL 11.5.1, FLINT 3.0.1
    sympy    1.14.0
