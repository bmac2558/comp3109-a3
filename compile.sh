#!/bin/bash
set -e

BUILD_DIR=build
ANTLR_JAR=antlr-3.1.2.jar

if [ ${#} != 1 ]; then
    echo "Usage: ${0} filename.vpl" >&2
    exit 1
fi

# check for the existance of BUILD_DIR
[ -d "${BUILD_DIR}" ] || mkdir ${BUILD_DIR}

# builds the ANTLR-generated parser using the grammar file
java -cp ${ANTLR_JAR} org.antlr.Tool -o ${BUILD_DIR} VPL.g
touch ${BUILD_DIR}/__init__.py

# uses the ANTLR-generated parser to convert the VPL program to ASM
./vpl2asm.py < ${1} > ${1}.s

# compiles the ASM and C file together
gcc -Wall -W main.c ${1}.s -o a3
