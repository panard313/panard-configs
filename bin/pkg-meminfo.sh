#!/bin/bash

echo "args:" $1 $2

list=`cat ~/PycharmProjects/perf/Apps_cn_25.txt`
acts=`echo $list |awk -F ':' '{print $2}'`
devs=`adb devices|grep -v List |awk '{print $1}'`

for i in `echo $acts`
do
    act=$i
    pkg=`echo $act|awk -F '/' '{print $1}'`
    for d in $devs
    do
        adb -s $d shell am start -S -W $i
        sleep 60
        adb -s $d shell dumpsys meminfo > meminfo-$pkg-$cnt
    done
done

#pkg=camera;cnt=1;for i in ;do adb -s $i shell am start -S -W com.mediatek.hz.camera/com.android.camera.CameraLauncher;sleep 5;adb -s $i shell dumpsys meminfo > meminfo-$i-$pkg-$cnt;done`')}'`
