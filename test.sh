#!/bin/bash

TESTDIR=tests
TMPFILE=/tmp/comp3109_ajan_bmac_test_tmpfile
PYTHON=python

for testdir in ${TESTDIR}/*; do
    if [ ! -d "${testdir}" ]; then
        echo -ne '\E[33m'  # yellow
        echo "${testdir} is not a directory."
        echo -ne '\E[0m'
        continue
    fi

    testname="$(echo "$testdir" | sed "s/.*\///")"

    echo "Compiling VPL and C in ${testdir}..."

    vplfile="${testdir}/${testname}.vpl"
    cfile="${testdir}/${testname}.c"

    if [ ! -f "${vplfile}" ]; then
        echo -ne '\E[33m'  # yellow
        echo "Skipping test dir ${testname}: missing vpl file at ${vplfile}"
        echo -ne '\E[0m'
        continue
    fi

    [ -f "${cfile}" ] || cfile="main.c"

    ./compile.sh ${vplfile} ${cfile}

    if [ $? -ne 0 ]; then
        echo -ne '\E[31m'  # red
        echo "${testname}: failed to compile"
        echo -ne '\E[0m'
        continue
    fi


    echo "Running tests in ${testname}..."

    for tfile in ${testdir}/input.*; do
        chknum="$(echo $tfile | sed 's/.*\.//')"
        infile="${testdir}/input.${chknum}"
        outfile="${testdir}/output.${chknum}"

        if [ ! -f "${outfile}" ]; then
            echo -ne '\E[33m'  # yellow
            echo "  Skipping input file ${infile}: missing ${outfile}"
            echo -ne '\E[0m'
            continue
        fi

        ./a3 < ${infile} > ${TMPFILE}
        diff ${TMPFILE} ${outfile}

        if [ $? -eq 0 ]; then
            echo -ne '\E[32m'  # green
            echo "  ${testname}.${chknum}: passed"
            echo -ne '\E[0m'
        else
            echo -ne '\E[31m'  # red
            echo "  ${testname}.${chknum}: failed"
            echo -ne '\E[0m'
        fi
    done
done

rm ${TMPFILE}
