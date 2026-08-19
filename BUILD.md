# BUILD

## System packages

```
apt-get update
apt-get install -y build-essential autoconf automake libtool pkg-config \
  libgmp-dev libmpfr-dev libntl-dev libflint-dev libcdd-dev libreadline-dev \
  poppler-utils bison flex time
```

## msolve 0.10.1

```
mkdir -p /opt/src && cd /opt/src
git clone --depth 1 --branch v0.10.1 https://github.com/algebraic-solving/msolve.git
cd msolve
./autogen.sh
./configure --prefix=/usr/local
make -j4
make install
echo /usr/local/lib > /etc/ld.so.conf.d/msolve.conf
ldconfig
```

## Singular 4.3.2p16

```
cd /opt/src
git clone --depth 1 --branch Release-4-3-2p16 https://github.com/Singular/Singular.git singular
cd singular
./autogen.sh
./configure --prefix=/usr/local
make -j4
make install
```

## Verification

```
Singular --version
msolve -h | head -5
```

## Reruns

```
mkdir -p reruns
for f in $(find wave0 wave1 -name '*.py' | sort); do
  timeout 900 python3 "$f" > "reruns/$(basename $f).log" 2>&1
done
```

## Papers

```
mkdir -p papers && cd papers
for id in 1901.04073 2204.14178 1902.05923 1401.1784 1605.09430 2608.00222; do
  curl -sSL -o "${id}.pdf" "https://arxiv.org/pdf/${id}"
done
sha256sum *.pdf > SHA256SUMS
```

## Figures

```
cd papers
mkdir -p figures_borisov figures_gghv
pdftoppm -r 200 -png 1901.04073.pdf figures_borisov/borisov
pdftoppm -r 200 -png 2204.14178.pdf figures_gghv/gghv
```
