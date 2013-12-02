#!/bin/sh
~/uwsgi26 -w run_uwsgi -p 4 -M -t 20 -R 10000 -d /home/www/log/conf_uwsgi.log --pidfile /home/www/conf_uwsgi.pid  -s 127.0.0.1:9310
