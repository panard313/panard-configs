#!/bin/bash


#rm -rf ~/tmp/cam_test/screen_cam_*.png

cnt=0
pid=0
current_file=NULL
while [ $cnt -le 5000 ]
do
    current_file=screen_cam_hdmiin_${cnt}_`date +%H-%M-%S`
    current_log=$current_file.log
    adb logcat -c
    sleep 0.5
    adb logcat -v time > ~/tmp/cam_test/$current_file.log &
    adb shell am start com.android.camera2/com.android.camera.CameraActivity
    sleep 5
    #adb shell screencap -p /sdcard/screen.png;adb pull /sdcard/screen.png ~/tmp/cam_test/screen_cam_hdmiin_${cnt}_`date +%H-%M-%S`.png
    adb shell screencap -p /sdcard/screen.png;adb pull /sdcard/screen.png ~/tmp/cam_test/$current_file.png
    if [ `ls -l $current_file.png |awk '{print $5}'` -le 8000 ]; then
        echo $current_file.png too small ......    stop test!!!
        kill -9 `ps aux |grep logcat |grep time|awk '{print $2}'`
        exit -100
    fi
    sleep 0.5
    #adb shell input keyevent 3
    #sleep 0.5
    #adb shell input keyevent 3
    #sleep 0.5
    #adb shell input keyevent 3
    #sleep 0.5
    pid=`adb shell ps |grep camera2|awk '{print $2}'`
    echo pid=$pid
    #adb shell kill $pid
    #sleep 5
    #adb shell kill $pid
    #adb shell am stop com.android.camera2/com.android.camera.CameraActivity
    adb shell input keyevent 4
    sleep 2
    kill -9 `ps aux |grep logcat |grep time|awk '{print $2}'`
    let cnt=$cnt+1;
done
