# Env setup
* ```conda env create -f environment.yaml``` after changing the envs path to yours
# Rest
## Local
* Server : ```cd rest/FL_Server && python3 manage.py runserver```
* Clients : ```cd rest && python3 run_local.py```
    * args
        * ip : host ip (public ip for remote)
        * client : number of participating clients
        * exp : 1, 2, 3, 4
        * round : number of rounds
        * num : number of samples per client 
        * delay : time delay until next command  
        
## Jetson
* Server : ```cd rest/FL_Server && python3 manage.py runserver 0.0.0.0:20000 ```
* Clients : 
    * ```docker pull crazyboy9103/jetson_fl:latest```
    * ```docker run -ti -p 20000:20000 crazyboy9103/jetson_fl:latest```
    * ```cd /FL/rest && python3 run_local.py --ip SERVER_IP --port 20000```

# TCP
## Local
* Server :  ```cd socket && python3 multi_server.py```
    * args
        * exp : 1, 2, 3, 4
        * num : number of samples per client
        * cli : number of participating clients
        * round : number of rounds
        * data : data mnist|cifar
        * host : host address (0.0.0.0 for remote)
        * port : port (forwarded port for remote)
        * epochs : number of local epochs
        * batch : size of batch

* Clients : ```cd socket && python3 test_multi_clients.py```
    * args
        * host : host address (public ip for remote)
        * port : port (forwarded port for remote)
        * cli : number of participating clients        
        
## Jetson
* Server : ```python multi_server.py --host 0.0.0.0 --port 20000```

* Clients :
    * ```docker pull crazyboy9103/jetson_fl:latest```
    * ```docker run -ti -p 20000:20000 crazyboy9103/jetson_fl:latest```
    * ```cd /FL/socket && python3 test_multi_clients.py --host SERVER_IP --port 20000```

