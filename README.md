# Env setup
* ```conda env create -f environment.yaml``` after changing the envs path
# Rest
* Server : ```cd rest/FL_Server && python manage.py runserver```
* Clients : ```cd rest && python run_local.py```

# TCP
* Server :  ```cd socket && python multi_server.py```
    * args
        * exp : 1, 2, 3, 4
        * num : number of samples each client sees
        * cli : number of participating clients
        * round : number of rounds
        * data : data mnist|cifar
        * host : host address (0.0.0.0 for remote)
        * port : port (forwarded port for remote)
        * epochs : number of local epochs
        * batch : size of batch
* Clients : ```cd socket && python test_multi_clients.py```
