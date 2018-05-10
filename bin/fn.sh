#!/bin/bash
#set -x
set -o noglob

#echo $*
if [ $# -gt 2 ]; then
    find $1 -name "$2"
else
    find . -name $1
fi


#set +x
set +o noglob
