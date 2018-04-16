#!/bin/bash

slid_right()
{
    adb shell input swipe 100 500 1000 500
}

slid_left()
{
    adb shell input swipe 1000 500 100 500
}

cnt=0
while [ 1 -eq 1 ] ; do
    let cnt=$cnt+1
    echo the $cnt time....
    slid_left
    sleep 0.1
    slid_left
    sleep 0.1
    slid_right
    sleep 0.1
    slid_right
    sleep 0.1
done
