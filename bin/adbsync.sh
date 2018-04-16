#!/bin/bash

echo "sync adb device now"
echo "ANDROID_PRODUCT_OUT=$ANDROID_PRODUCT_OUT"
/usr/bin/adb root
sleep 2
/usr/bin/adb remount;/usr/bin/adb sync system;/usr/bin/adb shell sync;/usr/bin/adb shell reboot
