#! /bin/sh
### BEGIN INIT INFO
# Provides:          python_spreadsheet_service
# Required-Start:
# Required-Stop:
# Default-Start:
# Default-Stop:      6
# Short-Description: Start/stop my pytohn spreadsheet service
# Description:
### END INIT INFO

PATH=/sbin:/usr/sbin:/bin:/usr/bin

#. /lib/lsb/init-functions

run=/home/chuck/home/git/python_spreadsheet/start.py

case "$1" in
  start)
	if [ "$(id -u)" != "0" ]; then
		echo "This script must be run as root" 1>&2
		exit 1
	fi
	python $run -b &
	echo "Started python spreadsheet service"
	;;
  restart|reload|force-reload)
	echo "Error: argument '$1' not supported" >&2
	exit 3
	;;
  stop)
	python /home/chuck/home/git/python_spreadsheet/stop.py
	echo "Stopped python spreadsheet service"
	;;
  *)
	echo "Usage: $0 start|stop" >&2
	exit 3
	;;
esac
