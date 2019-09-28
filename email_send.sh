#!/usr/bin/env bash
PATH=/home/yanlong/.pyenv/shims:/home/yanlong/.pyenv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
cd /home/yanlong/test/email_test
/usr/bin/expect <<-EOF
spawn git clone -b master "https://github.com/yanlong1993/iboy.git"
expect "Username*"
send "yanlong1993\n"
expect "Password*"
send "*zuozeixinxu0707\n"
expect eof
EOF
python /home/yanlong/test/email_test/iboy/email_test.py
echo OK


nohup /home/yanlong/test/email_test/email_send.sh >/dev/null 2>&1 &