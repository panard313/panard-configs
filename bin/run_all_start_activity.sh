#!/bin/bash
#set -x

if [ $# -gt 0 ]; then
    if [ x"$1" = x"-h" ]; then
        echo "Usage:"
        echo "    run_all_start_activity.sh [-h] [save_to_file]"
        echo "       -s: system apps only"
        echo "       -t: third party apps only"
        echo "       -h: print this message"
        echo "       save_to_file: file name to save launch time, default run_all_start_activity.log"
        exit 0
    elif [ x"$1" = x"-s" ]; then
        sys_only=y
        third_only=n
    elif [ x"$1" = x"-t" ]; then
        third_only=y
        sys_only=n
    else
        third_only=n
        sys_only=n
    fi

    if [ $# -eq 2 ]; then
        of=$2
    fi
    if [ $# -eq 1 ]; then
        arg1=$1
        if [ ${arg1:0:1} != "-" ]; then
            of=$1
        else
            of=run_all_start_activity.log
        fi
    fi
else
    of=run_all_start_activity.log
fi


a=0
for i in `adb shell cmd package list packages|awk -F ':' '{print $2}'`
do
    is_sys=n
    is_third=n
    if [ $sys_only = "y" ] || [ $third_only = "y" ]; then
        flag=`adb shell dumpsys package $i |grep -v "permission"|grep "flags="|sed 's/ //g'`
        #echo "flag=$flag"
        #if [ x"$flag" = *"SYSTEM"* ]; then
        ret=$(echo $flag|grep "SYSTEM")
        if [ x"$ret" != x"" ]; then
            is_sys=y
        else
            is_third=y
        fi
    fi

    if [[ ($sys_only = "y" && x$is_sys = x"y") || ($third_only = "y" && x$is_third = x"y") || ($sys_only = "n" && $third_only = "n") ]]; then
        act=`adb shell cmd package resolve-activity --brief $i|tail -n 1`
        if [ "$act" != "No activity found" ]; then
            echo got act: $act
            act_list[$a]=$act
            let a=$a+1
        fi
    fi
done


rm -rf $of

for act in ${act_list[@]}
do
    echo start act $act
    adb shell am start -S -W $act @ >> $of
    sleep 5
    adb shell input keyevent 3
    sleep 3
done

set +x
