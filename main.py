#!/usr/bin/env python
# coding=utf-8
from flask import Flask, request, render_template, jsonify, json
from flask_sqlalchemy import SQLAlchemy

mysql_host = "localhost"
mysql_db = "user"
mysql_username = "root"
mysql_password = "175@game"
 
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(mysql_username,mysql_password,mysql_host,mysql_db)
 
db = SQLAlchemy(app,use_native_unicode="utf8")
 
 
 
class external(db.Model):
  __tablename__ = 'external'
  user_id = db.Column(db.String(100), primary_key = True)
  user_name = db.Column(db.String(100))
  user_group = db.Column(db.String(100))
  host_ip = db.Column(db.String(100))
  host_name = db.Column(db.String(100))
  user_key = db.Column(db.String(800))
 

class internal(db.Model):
  __tablename__ = 'internal'
  user_id = db.Column(db.String(100), primary_key = True)
  user_name = db.Column(db.String(100))
  user_group = db.Column(db.String(100))
  host_ip = db.Column(db.String(100))
  host_name = db.Column(db.String(100))
  user_key = db.Column(db.String(800)) 
 
 
 
@app.route('/scanexternal/<key>', methods=['GET'])
def scanexternal(key):
     result = external.query.filter((external.user_name.like('%'+key+'%')) | (external.host_name.like('%'+key+'%')) | (external.host_ip.like('%'+key+'%')) | (external.user_group.like('%'+key+'%')))
     if result is None:
            json_result={"0":[{"user_name":None}]}
            print json_result
            return json.dumps(json_result,ensure_ascii=False)
     else:
            list_result=[]
            for i in result:
                host_rename = i.host_name.split("(")[0]+"<br>"+i.host_name.split("(")[1][:-1]
                tmp = {'user_name': i.user_name, 'host_name': host_rename, 'user_group': i.user_group, 'host_ip': i.host_ip, 'user_key': i.user_key}
                list_result.append(tmp)
            list_result = sorted(list_result)
            json_result = { "0": list_result}
            return json.dumps(json_result,ensure_ascii=False)
             
             

@app.route('/scaninternal/<key>', methods=['GET'])
def scaninternal(key):
     result = internal.query.filter((internal.user_name.like('%'+key+'%')) | (internal.host_name.like('%'+key+'%')) | (internal.host_ip.like('%'+key+'%')) | (internal.user_group.like('%'+key+'%')))
     if result is None:
            json_result={"0":[{"user_name":None}]}
            return json.dumps(json_result,ensure_ascii=False)
     else:
            list_result=[]
            for i in result:
                host_rename = i.host_name.split("(")[0]+"<br>"+i.host_name.split("(")[1][:-1]
                tmp = {'user_name': i.user_name, 'host_name': host_rename, 'user_group': i.user_group, 'host_ip': i.host_ip, 'user_key': i.user_key}
                list_result.append(tmp)
            list_result = sorted(list_result)
            json_result = { "0": list_result}
            return json.dumps(json_result,ensure_ascii=False)



@app.route('/')
def index():
    return render_template('external.html')
 
@app.route('/internal')
def change():
    return render_template('internal.html')
 
if __name__ == '__main__':
  app.run(host='0.0.0.0', port = 9090, debug=True)
