#!/bin/sh

cnt=0

while [ `encrp_test` -eq 0 ] ; do
    let cnt=$cnt+1
    echo the $cnt th time 
    #sleep 0.1
done
