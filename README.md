# stack
Stack configuration

docker-compose.yml : production stack for influxdb-grafan-nodered dashboard.
docker-compose.dummy.yml : dummy services for tests, which simulate the behaviour of a high-voltage power supply, a low-voltage power supply, and an environmental sensor. 
the repository images taken directly from github organization

To start the stack:
cd docker/tracker_dcs_stack/
docker compose -f docker-compose.yml -f docker-compose.dummy.yml up -d 

To check the running services:
docker compose ps 

IMAGE                                  COMMAND                    STATUS         PORTS                              NAMES
ghcr.io/cdozen/dummy:0.0.1             "python dummy/hv.py …"     Up 3 minutes                                      tracker_dcs_stack-lv-1
ghcr.io/cdozen/tracker_dcs_web:0.0.2   "uvicorn tracker_dcs…"     Up 3 minutes   8001/tcp, 0.0.0.0:8001->8000/tcp   tracker_dcs_stack-web_server-1
ghcr.io/cdozen/dummy:0.0.1             "python dummy/sensor…"     Up 3 minutes                                      tracker_dcs_stack-sensor_1-1
ghcr.io/cdozen/dummy:0.0.1             "python dummy/hv.py …"     Up 3 minutes                                      tracker_dcs_stack-hv-1
eclipse-mosquitto:2.0                  "/docker-entrypoint.…"     Up 3 minutes   0.0.0.0:1883->1883/tcp             tracker_dcs_stack-mosquitto-1
influxdb:2.0                           "/entrypoint.sh infl…"     Up 3 minutes   0.0.0.0:8086->8086/tcp             tracker_dcs_stack-influxdb-1
telegraf                               "/entrypoint.sh tele…"     Up 3 minutes   8092/udp, 8125/udp, 8094/tcp       tracker_dcs_stack-telegraf-1
grafana/grafana                        "/run.sh"                  Up 3 minutes   0.0.0.0:3000->3000/tcp             tracker_dcs_stack-dashboard-1


