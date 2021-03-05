# install git
sudo yum install git

# add nginx repository
sudo yum install epel-release
# install nginx
sudo yum install nginx
# start nginx
sudo systemctl start nginx
# allow http and https traffic
sudo firewall-cmd --permanent --zone=public --add-service=http 
sudo firewall-cmd --permanent --zone=public --add-service=https
sudo firewall-cmd --reload

# enable mysql repository
yum localinstall
https://dev.mysql.com/get/mysql57-community-release-el7-9.noarch.rpm

# install mysql 5.7 server
yum install mysql-community-server

# start mysql service
service mysqld start

# DIY: get temporary password
# sudo grep 'A temporary password' /var/log/mysqld.log |tail -1
# -> ==J1moqiA0aB -> changed to Foody$123

#initial mysql configuration
/usr/bin/mysql_secure_installation


# install memcached
yum update
yum install memcached

# install libmemcaced (tools to manage Memcached server)
yum install libmemcached

# run memcached
systemctl start memcached

# install python and tools
yum install python-devel python-setuptools python-pip

# install virtualenv
python -m pip install virtualenv

# install development tool
sudo yum groupinstall 'Development Tools'

# install package
pip install -r requirements.txt

# install for mysqlclient-dev
yum install mariadb-devel


# start all tools before start
systemctl start nginx
systemctl start mysqld
systemctl start memcached
systemctl start uwsgi

# change dir to the project dir, activate and install requirements in virtualenv
source venv/bin/activate
pip install -r requirements.txt

# running seeds db (create db and run initialize_db.sql before running seed)
python manage.py seed

