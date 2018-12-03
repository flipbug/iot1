#!/bin/sh
if [ -z $DEVPI ]; then 
  echo -n "Please enter Rasperry Pi IP: "
  read DEVPI;
fi

rsync -avhz --update . $DEVPI:/home/pi/megasec/
