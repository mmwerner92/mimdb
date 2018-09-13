#!/bin/bash

yum install -y httpd

sudo yum install -y gcc openssl-devel bzip2-devel wget
sudo yum install -y make git
cd /opt
command -v python2.7 || {
    wget https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz
    tar -xzf Python-2.7.11.tgz
    cd Python-2.7.11
    sudo ./configure --enable-optimizations
    sudo make altinstall
}
sudo yum install -y mysql-devel