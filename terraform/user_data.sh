#!/bin/bash
yum update -y
yum install -y git python3 pip
pip3 install boto3
cd /home/ec2-user
git clone https://github.com/a972k/POKEAPI-GAME.git
echo "cd /home/ec2-user/POKEAPI-GAME" >> /home/ec2-user/.bashrc
echo "python3 main.py" >> /home/ec2-user/.bashrc
