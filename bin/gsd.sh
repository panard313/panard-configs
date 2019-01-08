#!/bin/bash

if [ $# != 1 ]; then
    echo usage: gsd commit_id
    exit -1;
fi

OIFS="$IFS"
IFS=$'\n'
select var in `git d --name-only $1~1 $1`
do
    cd `git rev-parse --show-toplevel`
    git d $1~1 $1 $var
    cd -
    break
done
IFS="$OIFS"

