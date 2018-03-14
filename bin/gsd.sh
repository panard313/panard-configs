#!/bin/bash

if [ $# != 1 ]; then
    echo usage: gsd commit_id
    exit -1;
fi

select var in `git d --name-only $1~1 $1`
do
    git d $1~1 $1 $var
    break
done

