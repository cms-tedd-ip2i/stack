# SSH Tunnel to the DCS PC

The DCS PC lyovis12 is on the lab network. To connect to this PC from outside the lab, 
one must first establish an ssh connexion to the portal server, lyoserv. 

A typical way to connect via ssh from outside is to : 

* log in to lyoserv from outside 
* log in to lyovis12 from lyoserv

In this section, we will see how to use ssh to forward a port from a local machine 
outside the lab to lyovis12. 

This is will make it much more comfortable to use grafana and nodered from outside.

## Identify the port for your service

For example, here is the docker ps output for grafana: 

```bash
...  0.0.0.0:3001->3000/tcp, :::3001->3000/tcp             stack-grafana-1
```

We see that: 

* grafana runs on port 3000 in the grafana container.
* this port is mapped to port 3001 on the host machine lyovis12
* this port is accessible from anywhere, as indicated by the `0.0.0.0`

We can confirm the list of open ports on lyovis12 with the `lsof` command: 

```bash
lsof -i -P -n | grep LISTEN | grep 3001 
docker-pr 180921    root    4u  IPv4 1574869      0t0  TCP *:3001 (LISTEN)
docker-pr 180927    root    4u  IPv6 1574872      0t0  TCP *:3001 (LISTEN)
```

## Connect from within the lab network

It is thus possible to access grafana from the lab network.

To confirm, log into lyoserv, and run: 

```bash
curl lyovis12:3001
```

This gives the following response, which indicates that the service is reachable: 

```bash
<a href="/login">Found</a>.
```

## Establish the tunnel 

From your local machine outside the lab, do: 

```bash
ssh -L 3002:lyovis12:3001 lyoserv.in2p3.fr
```

This command will:  

* log you in to lyoserv
* forward port 3002 on your local computer to port 3001 on lyovis12 through lyoserv

This SSH tunnel is fully secure, and you can now connect to grafana on lyovis12 
from the browser of your local machine outside the lab. 

For this, just go to [http://localhost:3002](http://localhost:3002)


## Forward several ports 

You can forward several ports in one go to access different services.
For example, we can forward both the grafana and nodered ports by doing: 

```bash 

```



