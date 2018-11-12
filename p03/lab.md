# Lab 03

## Pub/Sub

### Simple Pub/Sub

```
mosquitto_sub -h 127.0.0.1 -p 1883 -t "#" -v
mosquitto_pub -h 127.0.0.1 -p 1883 -t "172.16.32.78/sensors/button0" -m "hello world"
```

### Pub/Sub with more specific wildcards

All hdd temperatures:
```
mosquitto_sub -h 127.0.0.1 -p 1883 -t "/machines/+/sensors/temperature/hdds/+" -v
```

Data from all sensors:
```
mosquitto_sub -h 127.0.0.1 -p 1883 -t "/machines/+/sensors/#" -v
```

### CPU Load

Generating many messages quickly results in a CPU load of 100%

## User Auth

Edit conf at /etc/mosquitto/mosquitto.conf:
```
allow_anonymous false
password_file /home/pi/mosquitto
```

Add user
```
mosquitto_passwd -c /home/pi/mosquitto_passwords user1
```

Start mosquitto and pub/sub with user authentication:
```
sudo mosquitto -c /etc/mosquitto/mosquitto.conf
mosquitto_sub -h 127.0.0.1 -p 1883 -t "#" -v -u user1 -P user1
mosquitto_pub -h 172.16.32.78 -p 1883 -t "172.16.32.78/sensors/button0" -m "hello world" -u user1 -P user1
```


