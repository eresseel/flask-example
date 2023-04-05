# flask-example

## Prepare dev environment
```bash
python3 -m venv .venv or virtualenv -p python3 .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## Run dev environment
```bash
flask run
```

## Accessing redis in a development environment
```bash
kubectl expose -n kube-application pod/redis-master-0 --port 6379 --type=NodePort
minikube ip
kubectl get -n kube-application svc --selector="statefulset.kubernetes.io/pod-name=redis-master-0" --output json | jq -r '.items[0].spec.ports[0].nodePort'
```
Assign the appropriate value to the variables in the .env file
export REDIS_PASSWORD="<password>"