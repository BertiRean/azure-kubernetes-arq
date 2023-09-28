local_master:
	kubectl apply -f ./kubernetes/local/spark-master-deployment.yaml
	kubectl apply -f ./kubernetes/local/spark-master-service.yaml


test_py:
	python ./tests/test.py

local_worker:
	kubectl apply -f ./kubernetes/local/spark-worker-deployment.yaml
	kubectl apply -f ./kubernetes/local/spark-worker-service.yaml

restart: delete local_master
	echo "Restarted"

log_master:
	kubectl logs deployment/spark-master -c spark-master

log_worker:
	kubectl logs deployment/spark-worker -c spark-worker

delete:
	kubectl delete all --all

build:
	docker build -f docker/Dockerfile -t spark-hadoop:3.2.0 ./docker

get_cluster_credentials:
	az aks get-credentials --resource-group spark-uade --name spark-cluster

list_cluster:
	az aks list --resource-group spark-uade

start_cluster:
	az aks start --resource-group spark-uade --name spark-cluster

stop_cluster:
	az aks stop --resource-group spark-uade --name spark-cluster

az_master:
	kubectl apply -f ./kubernetes/azure/spark-master-deployment.yaml
	kubectl apply -f ./kubernetes/azure/spark-master-service.yaml

az_worker: az_master
	kubectl apply -f ./kubernetes/azure/spark-worker-deployment.yaml

delete_az:
	kubectl.exe delete -f .\kubernetes\azure\spark-master-deployment.yaml
	kubectl.exe delete -f .\kubernetes\azure\spark-master-service.yaml
	kubectl.exe delete -f .\kubernetes\azure\spark-worker-deployment.yaml

delete_az_worker:
	kubectl.exe delete -f .\kubernetes\azure\spark-worker-deployment.yaml