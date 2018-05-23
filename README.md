# 图书管理系统说明

## 说明
* 这个是数据库引论的课程pj，里面还有许许多多需要改进的地方
* 技术栈：Django + Bootstrap + Mysql

## 实现功能：
1. 用户注册、登陆
2. 借书还书
3. 查找图书
4. 续借
5. 过期提醒
6. 多次过期惩罚
7. 新书推荐
8. 依照用户喜好推荐图书
9. 图书打分评论
10. 同样类别图书推荐

## 部署运行
### 链接数据库
1. 打开`books/books/settings.py`
2. 修改```
		DATABASES = {
    		'default': {
        		'ENGINE': 'django.db.backends.mysql',
        		'NAME': 'your_database_name',
        		'HOST': 'your_host',
        		'PORT': 'your_host',
        		'USER': 'your_username',
        		'PASSWORD': 'your_password'
    		}
		}```
	把其中your_*的内容改为你数据库的信息
3. 终端路径到`books/`
4. 终端输入`python manage.py makemigrations`
5. 终端输入`python manage.py migrate`


### 创建管理员用户
1. 终端路径到`books/`
2. 终端输入`python manage.py createsuperuser`
3. 根据提示建立用户信息

### 运行
1. 将终端路径改到`books`下（有manage.py的books）
2. 在终端输入`python manage.py runserver`


### 导入图书信息
1. 直接在数据库中录入
	* 使用mysql终端或者mysqlworkbench导入数据
2. 使用管理员用户录入
	1. 运行图书管理系统
	2. 进入管理员登陆界面并登陆
	3. 依照图形界面添加图书、作者、出版社、类别等信息
