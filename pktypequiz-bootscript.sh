#!/bin/bash
# This script is an initialization script to be used when creating a EC2 instances. The script installs all dependencies, fetches source code, and launches a server listening on port 80.
# install httpd (Linux 2 version)
yum update -y

#install
yum install -y httpd
yum install -y tmux
yum install -y git
yum install python3-pip -y

#pip install
pip3 install python-Levenshtein

#create a new directory to import YogonDexLite files
mkdir -p ydl
cd ydl

git clone https://github.com/yeohgi/PokemonTypeQuiz.git .

#create a new tmux session to let the server run indefinitly
tmux new-session -d -s myserver "python3 server.py 80"