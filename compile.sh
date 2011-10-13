#!/bin/sh
set -e

if [ ${#} -lt 1 ]; then
    echo "usage: ${0} vpl-file [c-file]"
    exit 1
fi

OUT_FILE=a3

vplfile=test.vpl
cfile=main.c
cflags="-Wall -W -std=c99 -g -O0"

[ -n "${1}" ] && vplfile="${1}" && shift 1
[ -n "${1}" ] && cfile="${1}" && shift 1
[ ${#} -gt 0 ] && cflags="${cflags} ${@}"

make -s

python vpl2asm.py $vplfile > $vplfile.s

if [ $? -ne 0 ]; then
    exit 1
fi

gcc ${cflags} ${cfile} ${vplfile}.s -o ${OUT_FILE}

if [ $? -ne 0 ]; then
    exit 1
fi

echo Done.
exit 0
