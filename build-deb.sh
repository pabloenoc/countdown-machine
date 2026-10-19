#!/bin/sh
set -eu
cd "$(dirname "$(readlink -f "$0")")"

VERSION=1.0.1
STAGE=build/countdown-machine_$VERSION

rm -rf build
mkdir -p "$STAGE/DEBIAN"
cp -r usr "$STAGE/"

# Normalize permissions: folders 755, files 644, programs 755
find "$STAGE/usr" -type d -exec chmod 755 {} +
find "$STAGE/usr" -type f -exec chmod 644 {} +
chmod 755 "$STAGE/usr/bin/countdown-machine" "$STAGE/usr/lib/countdown-machine/countdown-machine.py"

# Remove local development files
rm -f "$STAGE/usr/share/glib-2.0/schemas/gschemas.compiled"
rm -f "$STAGE"/usr/share/countdown-machine/*.ui~

cp packaging/control "$STAGE/DEBIAN/control"

dpkg-deb --build --root-owner-group "$STAGE"