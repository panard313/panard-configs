#!/usr/bin/env bash

usage(){
    echo "请输入命令参数选项"
}

#':ld:ft:'第一个冒号表示忽略错误；字符后面的冒号表示该选项必须有自己的参数
while getopts 'ld:ft:' OPT; do
    case ${OPT} in
        d)
            DEL_DAYS="$OPTARG";;
        f)
            DIR_FROM="$OPTARG";;
        t|l)
            DIR_TO="$OPTARG";;
        ?)
            #echo "Usage: `basename $0` [options] filename"
            usage
     esac
done

# getopts在处理参数的时候，处理一个开关型选项(不带值选项)，OPTIND加1，
# 处理一个带值的选项参数，OPTIND则会加2
if [[ $OPTIND -eq 1 ]]; then
    usage
fi
