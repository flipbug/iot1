#!/bin/sh
if [ -z $DEVPI ]; then 
  if [ -z $1 ]; then
    echo -n "Please enter Rasperry Pi IP: "
    read DEVPI;
    echo "set \`export DEVPI=<IP-Address>\` for persistent magic or run as ${0} <ip address>"
  else
    DEVPI=$1
  fi
fi

rsync -avhz --update . $DEVPI:/home/pi/megasec/
