#!/usr/bin/env python
# -*- coding:utf-8 -*-
# update users data in servers
import MySQLdb
from os import walk, path, getcwd, makedirs, _exit
import re, sys
import socket

ansible_external_hosts=sys.path[0]+"/external_hosts"
ansible_internal_hosts=sys.path[0]+"/internal_hosts"
user_data=sys.path[0]+"/user_data"
mysql_host = "localhost"
mysql_db = ""
mysql_username = ""
mysql_password = ""

def getdata(location, ansiblehost):
    data=[]
    for (dirpath, dirnames, filenames) in walk(user_data):
        if len(dirpath) == 0 or len(filenames) == 0 or filenames[0] == "unzip.sh" or filenames[0] == "clean_dir.sh":
            continue
        #print dirpath,filenames
        if dirpath.split("/")[-1] == dirpath.split("/")[-2]:
            host_name = "-"
        else:
            host_name = dirpath.split("/")[-2]  

        check_exists_user(location, dirpath.split("/")[-1], filenames)

        for user in filenames:
            with open(path.join(dirpath,user)) as f:
                user_conf_data = f.readlines()
            f.close()
            #print user_conf_data
            groupdata = user_conf_data[0].split()[2].split("=")[1].split(",")
            userkey = '\n'.join(user_conf_data[1:])
            tmp_list=[]
            for _ in groupdata:
                each_group = re.search("\d+\((.*)\)", _).group(1)
                tmp_list.append(each_group)
            usergroup=','.join(tmp_list)
            with open(ansiblehost) as g:
                for line in g:
                    if re.search(dirpath.split("/")[-2]+"\s+",line):
                        host_name_ip = line.split()[1].split("=")[1]
                        if re.search("(.*)\.com$", host_name_ip):
                            host_name_ip = socket.gethostbyname(host_name_ip)
                        break
                    else:
                        continue
                else:
                    host_name_ip = dirpath.split("/")[-1] 
            tmp = {"user_name": user, "user_group": usergroup, "host_ip": dirpath.split("/")[-1], "host_name": dirpath.split("/")[-2]+"("+host_name_ip+")", "user_key": userkey}
            data.append(tmp)
    #print len(data)
    updatedb(location, data)
    
    
def check_exists_user(location, host_ip, users):
    db = MySQLdb.connect(mysql_host,mysql_username,mysql_password,mysql_db )
    cursor = db.cursor()
    check_sql = "select user_name from %s where host_ip = '%s'"%(location, host_ip)
    try:
        cursor.execute(check_sql)
        results = cursor.fetchall()
        for row in results:
            if row[0] in users:
                continue
            else:
                delete_sql = "DELETE FROM %s where user_name = '%s' and host_ip = '%s'"%(location, row[0], host_ip)
                print "Database update : DELETE "+row[0]+"  in  "+host_ip
                cursor.execute(delete_sql)
                db.commit()
    except:
        db.rollback() 
    
    

def updatedb(location, data):
    db = MySQLdb.connect(mysql_host,mysql_username,mysql_password,mysql_db )
    cursor = db.cursor()
    for user_data in data:
        check_sql="select * from %s where user_name = '%s' and host_ip = '%s'"%(location, user_data["user_name"], user_data["host_ip"])
        cursor.execute(check_sql)
        if len(cursor.fetchall()) == 0:
            insert_sql="INSERT INTO %s(user_name, user_group, host_ip, host_name, user_key)VALUES ('%s', '%s', '%s', '%s', '%s')"%(location, user_data["user_name"], user_data["user_group"], user_data["host_ip"], user_data["host_name"], user_data["user_key"])
            try:
                cursor.execute(insert_sql)
                print "Database update : INSERT "+user_data["user_name"]+"   in    "+user_data["host_name"]
                db.commit()
            except:
                db.rollback()
        elif len(cursor.fetchall()) == 1:
            update_sql="UPDATE %s SET user_group='%s',host_name='%s',user_key='%s'"%(location, user_data["user_group"], user_data["host_name"], user_data["user_key"])
            try:
                cursor.execute(update_sql)
                print "Database update : UPDATE "+user_data["user_name"]+"   in    "+user_data["host_name"]
                db.commit()
            except:
                db.rollback()
        else:
            delete_sql="DELETE FROM %s where user_name = '%s' and host_ip = '%s'"%(location, user_data["user_name"], user_data["host_ip"])
            try:
                cursor.execute(delete_sql)
                db.commit()
            except:
                db.rollback()
            insert_sql="INSERT INTO %s(user_name, user_group, host_ip, host_name, user_key)VALUES ('%s', '%s', '%s', '%s', '%s')"%(location, user_data["user_name"], user_data["user_group"], user_data["host_ip"], user_data["host_name"], user_data["user_key"])
            try:
                cursor.execute(insert_sql)
                #print "Database update : REINSERT "+user_data["user_name"]+"   in    "+user_data["host_name"]+"     Because Repeat."
                db.commit()
            except:
                db.rollback()
    db.close()


def main(arg):
    if arg == 'external':
        getdata(arg, ansible_external_hosts)
    else:
        getdata(arg, ansible_internal_hosts)


if __name__ == "__main__":
    main(sys.argv[1])

