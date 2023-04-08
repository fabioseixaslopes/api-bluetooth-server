#!/bin/bash
set -x

#### wait, update time. ####
sudo su &
apt-get update

#### Python ####
apt-get install python2
#apt-get install python3 

#### PIP ####
apt-get install pip	#python 2
#apt-get install python3-pip	#python 3

#### install dependencies ####
pip install -r requirements.txt

#### bye ####
echo "all done."