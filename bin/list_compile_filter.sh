#!/bin/bash


for i in `adb shell cmd package list packages|awk -F ':' '{print $2}'`
do
    echo $i :
    echo `adb shell dumpsys package $i |grep status`
    echo
done
