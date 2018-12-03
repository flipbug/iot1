#!/bin/sh
if [ -z $DEVPI ]; then 
  echo -n "Please enter Rasperry Pi IP: "
  read DEVPI;
  echo "set \`export DEVPI=<IP-Address>\` for persistent magic"
fi

rsync -avhz --update . $DEVPI:/home/pi/megasec/
