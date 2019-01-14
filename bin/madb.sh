#!/bin/bash

echo args: $@
for i in `adb devices|grep -v attach|awk '{print $1}'`
do
    adb -s $i $@
done
