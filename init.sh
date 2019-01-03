#!/bin/sh

cd /root

if [ -f /secrets/id_rsa -a ! -f /root/.ssh/id_rsa ]; then
   cp /secrets/id_rsa /root/.ssh
fi


git config --global user.email "yeolhyun.kwon@gmail.com"
git config --global user.name "Yeolhyun Kwon"
git clone git@github.com:$GITHUB_USER/$GITHUB_REPO
