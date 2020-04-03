#!/bin/bash

power_key ()
{
    echo "input POWER key !!!!!!!!!!!!!" >> doze.log
    adb shell input keyevent 26
}

single_cycle ()
{
    total_time=720
    cnt=180
    for ((i=0;i<$cnt;i=i+1))
    do
        echo -------------------------$i-------------------------- >> $1
        echo `date +\"%Y-%m-%d_%H:%M.%S\"` >> $1
        adb shell dumpsys deviceidle|tail -n 20  >> $1
        sleep 5
    done
}

# make sure screen is off
screen_state=`adb shell dumpsys deviceidle |grep mState|awk '{print $1}'|awk -F '=' '{print $2}'`
if [ x$screen_state = xACTIVE ]; then
    power_key
    sleep 1
fi

while true
do
    single_cycle doze.log
    power_key
    sleep 5
    power_key
done
