# How to use lease-quinta

# Instalation
##Install over the current python instalation:

`pip install -r requirements.txt`

##Install over a virtual environment:

`python3 -m venv /path/to/quinta_client`

`source /path/to/quinta_client/bin/activate`

`python3 -m venv /path/to/quinta_client`



# Client
 `usage: client.py <user> -a {tryAcquireLease,history,checkLease,removeLease} [-k]`

 + **< user >** The name of the user
 + -a **< action >** Action that will be performed {tryAcquireLease,history,checkLease,removeLease}
 + -k **Keep Acquiring** flag will block and set a 24h timer after the initial lease expire, when the finishes using quinta terminating the program with Ctrl + C will remove the lease previously held.

## Pyhton Client examples:
* `client.py Joao -a tryAcquireLease` -- The user will be prompted with a couple of instructions used to build the request. 
* `client.py Joao -a tryAcquireLease -k ` -- The user will be prompted with a couple of instructions used to build the request. 
* `client.py Joao -a removeLease`
* `client.py Joao -a checkLease`
* `client.py Joao -a history` 

## cURL example:
* `curl -i -H "Content-Type: application/json" -X POST -d '{"machines": ["s1", "s2"],"time": "0:1","notes":"Nao interromper", "owner":"Joao"}' http://IP:80/tryAcquireLease`
* `curl -i  http://IP:80/checkLease`
* `curl -i http://IP:80/removeLease`
* `curl -i  http://IP:80/history`
