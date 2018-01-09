#!/bin/bash
# run this shell script for config ansible-playbook

set -e

env_location="/home/xxx/env"
location=$1
group=$2
if [ ! $location ];then
    echo "Lack of hosts type.(exp:  internal/external/all)"
    exit 2
fi


if [ "$location" = "all" ];then
    path="$( cd "$( dirname "$0"  )" && pwd  )"
    #echo "Beginning update [[ user ]] database...."

    echo "Begin From internal hosts..."

    for ingroup in $(grep -E "\[(.*)\]" internal_hosts|cut -d '[' -f2|cut -d ']' -f1)
    do
        sed -i "s/^.*hosts.*$/- hosts: \"$ingroup\"/g" Fetch_files.yml
        echo "Start fetch user data from internal servers..."
        sh $path/user_data/clean_dir.sh
        echo "Collecting user data from $ingroup..."
        $env_location/bin/ansible-playbook -i internal_hosts Fetch_files.yml  1>/dev/null 2>&1
        echo "Collect Done..."
        sh $path/user_data/unzip.sh
        echo "Updateing database..."
        $env_location/bin/python db_update.py internal
        echo "$ingroup----- Update Finished !"
        sleep 1
    done

    sh $path/user_data/clean_dir.sh

    echo "Grap date From external hosts..."

    for exgroup in $(grep -E "\[(.*)\]" external_hosts|cut -d '[' -f2|cut -d ']' -f1)
    do
        sed -i "s/^.*hosts.*$/- hosts: \"$exgroup\"/g" Fetch_files.yml
        echo "Start fetch user data from remote servers..."
        sh $path/user_data/clean_dir.sh
        echo "Collecting user data from $exgroup..."
        $env_location/bin/ansible-playbook -i external_hosts Fetch_files.yml  1>/dev/null 2>&1
        echo "Collect Done..."
        sh $path/user_data/unzip.sh
        echo "Updateing database..."
        $env_location/bin/python db_update.py external
        echo "$exgroup----- Update Finished !"
        sleep 1
    done

    sh $path/user_data/clean_dir.sh

else
    if [ ! $group ];then
        echo "Lack of hosts group.(exp:  qtz-ops)"
        exit 2
    fi


    path="$( cd "$( dirname "$0"  )" && pwd  )"
    #echo "Beginning update [[ user ]] database...."

    echo "Begin From $location hosts..."

    for gp in  $(grep -E "\[($group.*)\]" ${location}_hosts|cut -d '[' -f2|cut -d ']' -f1)
    do
        echo $gp
        sed -i "s/^.*hosts.*$/- hosts: \"$gp\"/g" Fetch_files.yml
        echo "Start fetch user data from remote servers..."
        sh $path/user_data/clean_dir.sh 
        $env_location/bin/ansible-playbook -i ${location}_hosts Fetch_files.yml 
        if [ $(ls $path/user_data/|grep -vE '.sh$'|wc -l) -eq 0 ];then
            echo "Not Found Any hosts"
            exit 2
        else
            echo "Collect Done..."
            sh $path/user_data/unzip.sh
            echo "Updateing database..."
            $env_location/bin/python db_update.py ${location}
            echo "$gp----- Update Finished !"
            sh $path/user_data/clean_dir.sh 
        fi
    done
fi
