#/bin/bash
# run by root

tip=$(sudo ifconfig|grep -iE 'mask.255.255.255.0'|grep 'inet '|grep -v '127.0'|xargs|awk -F ' ' '{print $2}'|cut -d':' -f 2|head -1)
if [ ! $tip ];then
    tip=$(sudo ifconfig|grep -iE 'mask.255.255.240.0'|grep 'inet '|grep -v '127.0'|xargs|awk -F ' ' '{print $2}'|cut -d':' -f 2|head -1)
    if [ ! $tip ];then
        tip=$(sudo ifconfig|grep -iE 'mask.255.255.248.0'|grep 'inet '|grep -v '127.0'|xargs|awk -F ' ' '{print $2}'|cut -d':' -f 2|head -1)
        if [ ! $tip ];then
            tip=$(sudo ifconfig|grep -iE 'mask.255.0.0.0'|grep 'inet '|grep -v '127.0'|xargs|awk -F ' ' '{print $2}'|cut -d':' -f 2|head -1)
            if [ ! $tip ];then
                tip=$(sudo ifconfig|grep -iE 'mask.255.255.0.0'|grep 'inet '|grep -v '127.0'|xargs|awk -F ' ' '{print $2}'|cut -d':' -f 2|head -1)
                if [ ! $tip ];then
                    tip=$(sudo ifconfig|grep -iE 'mask.255.255.255.224'|grep 'inet '|grep -v '127.0'|xargs|awk -F ' ' '{print $2}'|cut -d':' -f 2|head -1)
                    if [ ! $tip ];then
                         tip=$(sudo ifconfig|grep -iE 'mask.255.255.252.0'|grep 'inet '|grep -v '127.0'|xargs|awk -F ' ' '{print $2}'|cut -d':' -f 2|head -1)
                    fi
                fi
            fi
        fi
    fi
fi
if [ ! $tip ];then
    exit 1
fi
mkdir -p /tmp/grap_data/$tip
cd /tmp/grap_data
for user in $(cat /etc/passwd|awk -F ":" '{print $1}')
do
    user_info=$(id $user)
    if [ $? -eq 0 ];then
        ssh_pubkey=$(cat /home/$user/.ssh/authorized_keys > /dev/null)
        if [ $? -eq 1 ];then
            ssh_pubkey=$(cat /data/home/$user/.ssh/authorized_keys > /dev/null)
            if [ $? -eq 1 ];then
                continue
            else
                echo $user_info > /tmp/grap_data/$tip/$user
                for line in $(cat /data/home/$user/.ssh/authorized_keys);do
                    echo $line >> /tmp/grap_data/$tip/$user
                done
            fi
        else
            echo $user_info > /tmp/grap_data/$tip/$user
            for line in $(cat /home/$user/.ssh/authorized_keys);do
                echo $line >> /tmp/grap_data/$tip/$user
            done
        fi
    fi
done

tar zcf user_data.tar.gz $tip
mv user_data.tar.gz /tmp/
rm -rf /tmp/grap_data
