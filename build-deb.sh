#!/bin/sh
set -e
cd "$(dirname "$(readlink -f "$0")")"

VERSION=1.0.0
STAGE=build/countdown-machine_$VERSION

rm -rf build
mkdir -p "$STAGE/DEBIAN"
cp -r usr "$STAGE/"
rm -f "$STAGE/usr/share/glib-2.0/schemas/gschemas.compiled"
rm -f "$STAGE"/usr/share/countdown-machine/*.ui~
cp packaging/control "$STAGE/DEBIAN/control"

dpkg-deb --build --root-owner-group "$STAGE"
