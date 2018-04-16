#!/bin/bash


rm -rf ~/tmp/cam_test/screen_cam_*.png


adb shell am start com.android.camera2/com.android.camera.CameraActivity
sleep 4

cnt=0
while [ $cnt -le 2000 ]
do
    adb shell input tap 1055 295
    sleep 10
    adb shell screencap -p /sdcard/screen.png;adb pull /sdcard/screen.png ~/tmp/cam_switch/screen_cam_switch_${cnt}_`date +%H-%M-%S`.png
    sleep 1
    let cnt=$cnt+1;
done
