Sensor monitoring using Flask, MariaDB, jQuery
==============================================


Configuration
-------------

Sensor -- Arduino -- USB -- Pi -- Flask, MySQL, jQuery



Settings
--------

# Arduino
```
$ sudo apt install arduino
$ sudo usermod -a -G tty pi
$ sudo usermod -a -G dialout pi
```

# MariaDB
```
$ sudo apt install mysql-server mysql-client
or
$ sudo apt install mariadb-server mariadb-client

$ sudo service mariadb restart
$ sudo mysql -u root -p
```

```
mysql> use mysql;
mysql> select user, host, plugin from mysql.user;
mysql> CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';
mysql> UPDATE user SET plugin='mysql_native_password' WHERE user='admin';
mysql> FLUSH PRIVILEGES;

mysql> source schema.sql;
mysql> DESC sensors;
mysql> use conception;
```

# Flask
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```


Usage
-----
```
(venv) $ flask --app app --debug run
```
