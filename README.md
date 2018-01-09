# User-Management-System
# 服务器用户信息管理系统
This repository is build for store users' info in servers from servers and make it visible.

Github 开源项目地址： https://github.com/Polaris0112/User-Management-System ，欢迎Start ：）


## 简述
该项目是基于Flask编写的轻量级用户信息管理系统，通过python+ansible+shell组合来构造自动化抓取服务器上的用户信息并存入MySQL数据库中。最后用户可以在页面中，根据关键字查询是否存在对应的用户或者服务器，并能看到用户和服务器的一些简单信息如服务器名称，服务器外网IP、内网IP、用户名、用户组还有用户公钥。

效果图如下：



## 部署环境

-  CentOS6/CentOS7 （其他linux系统应该都可以，未测过）

-  python2.7.x

-  ansible

-  mysql

## 安装过程

-  安装好mysql，确定数据库名、数据库用户名和数据库密码

-  推荐：进入virtualenv，安装所需要的依赖包，`pip install -r requirement.txt`

-  需要修改以下几个文件：
  -  `db_update.py`：更改文件12-15行关于mysql数据库的配置，就是第一步创建的数据库和账号密码
  -  `main.py`：更改文件6-9行关于mysql数据库的配置，就是第一步创建的数据库和账号密码
  -  `update.sh`：更改文件第6行，把对应路径换成目前正在使用的virtualenv的绝对路径
  -  `./roles/fetch_files/tasks/main.yml`：更改文件第10行，把`dest`后的绝对路径换成当前路径并指向到`user_data`

-  **初始化数据库，执行`mysql -u [用户名] -p  [数据库名] < init_users.sql`**

-  修改`external_hosts`文件，这个文件是外网服务器的配置文件，可以根据已给出的例子作为模板来对应修改，第一列是服务器备注名，第二列对应的值改成能ssh到服务器的IP，若要修改其他属性项，请参考[这里](http://docs.ansible.com/ansible/latest/intro_inventory.html)

-  修改`internal_hosts`文件，这个文件是内网服务器的配置文件，操作同上

-  （如果需要域名访问）修改`user_uWSGI.ini`，把其中`home`对应的值改成当前使用的`virtualenv`的绝对路径

-  启动方式：`（进入env之后） python main.py` 即可
    注意：如果是通过域名访问的话，直接运行`uwsgi --ini user_uWSGI.ini`，不需要执行`main.py`



## 项目模块解释

-  `mian.py`：Flask主程序

-  `roles`：调用ansible的时候需要使用到的模块，里面有远程抓取时候的操作细节

-  `static`：网页用到的css、fonts、js文件

-  `templates`：本项目使用到的两个页面

-  `user_data`：存放抓取到的用户信息

-  `db_update`：对`user_data`里面的数据进行清洗，入库，更新数据库操作的工具

-  `Fetch_files.yml`：执行ansible的playbook

-  `external_hosts`：外网服务器的ansible hosts配置文件

-  `internal_hosts`：内网服务器的ansible hosts配置文件

-  `init_users.sql`：初始化表结构的sql数据库文件

-  `user_uWSGI.ini`：用于配置uwsgi的配置文件

-  `update.sh`：用于整合调用ansible抓取数据，并执行`db_update.py`入库的自动化工具



## 工具使用

-  假如你已经按照上述步骤配置好了，那么你的`external_hosts`文件和`internal_hosts`文件已经按照格式配置好，那么接下来就可以使用`update.sh`工具来进行数据的入库。（前提是可以从本机ssh到目标机器）
 ```bash
 用法1： 全更新
     sh update.sh all
	 这个操作会先读取内网服务器配置文件，然后抓取到的信息再清洗、更新入库
	 然后再读取外网服务器配置文件，进行相同的操作
 
 用法2：部分更新
     sh update.sh [location]  [group-name]
	 exp :   sh update.sh external test
	 第一个参数是代表当前需要更新的是内网服务器还是外网服务器，这个参数会根据你的选择来判断读取哪个配置文件，只能是external或internal，填入其他返回空结果
	 第二个参数是代表需要执行该内/外网服务器配置文件的哪一组服务器，如果你之前有看过ansible inventory的文件格式的话，不难发现是按组区分各类目标的，所以假如你是批量处理的话，直接填上组名就可以抓取该组下所有的服务器用户信息

 ```



## 交流、反馈和建议

-  邮箱：jjc27017@gmail.com

-  欢迎各位Fork和Star，也欢迎各位提issue，我会尽快回答



