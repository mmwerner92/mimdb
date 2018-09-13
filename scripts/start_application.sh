#!/usr/bin/env bash

cd /home/ec2-user/www/project/
source /home/ec2-user/www/project-venv/bin/activate
echo yes | /home/ec2-user/www/project/manage.py collectstatic
./manage.py runserver