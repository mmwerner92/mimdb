#!/usr/bin/env bash
chown ec2-user:ec2-user /home/ec2-user/www/project -R
cd /home/ec2-user/www/project/
#source /home/ec2-user/www/project-venv/bin/activate
chmod +x ./manage.py 
ls -al
./manage.py makemigrations
./manage.py migrate auth
./manage.py migrate
