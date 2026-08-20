# Opus worker setup (both sessions)

Clone and position:
```
git clone https://github.com/git-df-scott/jacobian_planar.git ~/w && cd ~/w
git checkout claude/opus-5-counterexample-plan-sep6yk
git fetch origin claude/fable-ce-backup
for f in resister_specs.json opus_regen.py d12slice_probe.py; do git show origin/claude/fable-ce-backup:jacobian/opus_kit/$f > /tmp/$f; done
```

Install Singular (apt) and msolve 0.10.1 (source):
```
sudo apt-get update && sudo apt-get install -y singular autoconf automake libtool libgmp-dev libmpfr-dev libflint-dev
mkdir -p /tmp/src && cd /tmp/src
git clone --depth 1 --branch v0.10.1 https://github.com/algebraic-solving/msolve.git
cd msolve && ./autogen.sh && ./configure && make -j4 && sudo make install && sudo ldconfig
msolve -h | head -3   # must print usage
Singular --version    # must print 4.x
python3 -c 'import sympy; print(sympy.__version__)'  # pip install sympy if missing
```

Reporting rules (both sessions): report RAW outputs only (first 60 bytes of each .out, timings, md5s). [-1] = EMPTY. Non-empty output = report the raw head IMMEDIATELY and clearly, do not interpret. 0-byte output or crash = FAILURE (not a verdict) - say so. If a control gate fails, STOP and report that instead of continuing.
