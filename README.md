# Tedd DCS stack

TODO:  

* write intro here

Stack configuration: 

* [docker-compose.yml](docker/tracker_dcs_stack/docker-compose.yml) : production stack with the core services: 
  * mosquitto : mqtt broker
  * web_server : for labview data ingestion
  * influxdb : time-series database
  * telegraf : ingests data from the mqtt broker into the database
  * dashboard : Grafana monitoring dashboard
  * low_voltage : Control of the Rhode and Schwartz low-voltage power supply

  **TODO: where is nodered ?** 
  

* [docker-compose.yml](docker/tracker_dcs_stack/docker-compose.dummy.yml) : additional dummy services for tests, which simulate the behaviour of a high-voltage power supply, a low-voltage power supply, and an environmental sensor. 

## Prerequisites

TODO : need links / more explanations here

* Install docker 
* Install docker-compose 

## Deploying the stack for the first time

Start the InfluxDB service: 

```
docker-compose up -d influxdb
```

Get your influxdb 

## Start the stack together with the dummy services 

```
cd docker/tracker_dcs_stack/
docker compose -f docker-compose.yml -f docker-compose.dummy.yml up -d 
```

To check the running services:

```
docker compose -f docker-compose.yml -f docker-compose.dummy.yml ps 
```

```
NAME                              COMMAND                  SERVICE             STATUS              PORTS
tracker_dcs_stack-dashboard-1     "/run.sh"                dashboard           running             0.0.0.0:3001->3000/tcp
tracker_dcs_stack-hv-1            "python dummy/hv.py …"   hv                  running             
tracker_dcs_stack-influxdb-1      "/entrypoint.sh infl…"   influxdb            running             0.0.0.0:8086->8086/tcp
tracker_dcs_stack-low_voltage-1   "python3 hmp.py lw_v…"   low_voltage         exited (1)          
tracker_dcs_stack-lv-1            "python dummy/hv.py …"   lv                  running             
tracker_dcs_stack-mosquitto-1     "/docker-entrypoint.…"   mosquitto           running             0.0.0.0:1884->1883/tcp
tracker_dcs_stack-sensor_1-1      "python dummy/sensor…"   sensor_1            running             
tracker_dcs_stack-telegraf-1      "/entrypoint.sh tele…"   telegraf            running             8125/udp
tracker_dcs_stack-web_server-1    "uvicorn tracker_dcs…"   web_server          running             0.0.0.0:8001->8000/tcp
```

## Start the production stack

```
cd docker/tracker_dcs_stack/
docker compose up -d 
```

## Using the services 

### Mosquitto

Subscribe to all topics: 

```
docker exec tracker_dcs_stack-mosquitto-1 mosquitto_sub -v -t /#
```

You should see the messages that are being sent by the dummy modules: 

```
/lv/status [{"number": 0, "on": 0, "vreq": 0.0}]
/hv/status [{"number": 0, "on": 0, "vreq": 0.0}]
/sensor_1/status {"meas1": -0.9931889975255942, "meas2": 0.9931889975255942}
...
```

You can also submit messages with `mosquitto_pub`. 

For more information, see the [Mosquitto documentation](https://mosquitto.org/documentation/).

### Grafana

Go to [http://localhost:3001](http://localhost:3001)

* username : admin
* password : admin 

Skip the creation of a new password

**TODO** : 

* add dashboard ! 
* how to connect to influxdb measurements ? 
* need to have the dashboard set up without any intervention from the user (influxdb connection and dashboard)

### InfluxDB

**TODO why is the port exposed? what is the user supposed to do with it ?**

### Nodered 

**TODO : where is nodered ?**

