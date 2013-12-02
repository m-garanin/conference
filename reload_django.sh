#!/bin/sh
### Reload django ###
kill -15 `cat /home/www/conf_uwsgi.pid`

