#!/bin/sh
cd "$(dirname "$(readlink -f "$0")")"
glib-compile-schemas --strict usr/share/glib-2.0/schemas/
GSETTINGS_SCHEMA_DIR=usr/share/glib-2.0/schemas exec ./usr/lib/countdown-machine/countdown-machine.py "$@"