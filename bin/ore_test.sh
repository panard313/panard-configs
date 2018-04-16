adb shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0

while true
do
adb shell content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:0
sleep 1
adb shell content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:1
sleep 1
adb shell content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:2
sleep 1
adb shell content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:3
sleep 1
done
