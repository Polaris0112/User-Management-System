#!/bin/bash

path="$( cd "$( dirname "$0"  )" && pwd  )"

for host in $(ls $path|grep -vE '.sh$')
do
    cd $path/$host/
    mv $path/$host/tmp/user_data.tar.gz  $path/$host/
    tar zxvf user_data.tar.gz 1>/dev/null 2>&1
    rm -rf $path/$host/tmp
    rm -rf $path/$host/user_data.tar.gz
done



