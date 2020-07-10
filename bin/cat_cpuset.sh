#!/bin/bash

function lscgroup() {
    type=$1
    if [[ -z $type ]];then
        type="cpuset"
    fi
    echo $type
    cg_list=`adb shell "find /dev/$type -type d"`
    echo "List of cgroups under /dev/$type:"
    for cg in $cg_list
    do
        if [[ $cg == /dev/$type ]];then
            cg="$cg/"
        fi
        case $type in
        "cpuset")
        value=`adb shell "cat $cg/cpus"`
        value="cpus:$value"
        ;;
        "blkio")
        value=`adb shell "cat $cg/blkio.weight"`
        value="blkio.weight:$value"
        ;;
        esac

        echo -e "$cg\t$value"| sed "s#/dev/$type\(.*\)#\t\1#g"
    done
}

lscgroup
