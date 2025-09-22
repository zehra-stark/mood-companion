#!/bin/bash
sudo yum install -y python3 python3-pip
python3 -m pip install --user --upgrade pip
python3 -m pip install --user -r /home/ec2-user/Mood_Companion_Lambda/requirements.txt

