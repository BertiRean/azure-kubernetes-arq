local_master:
	kubectl apply -f ./kubernetes/local/spark-master-deployment.yaml
	kubectl apply -f ./kubernetes/local/spark-master-service.yaml

local_worker:
	kubectl apply -f ./kubernetes/local/spark-worker-deployment.yaml

log_master:
	kubectl logs deployment/spark-master -c spark-master

log_worker:
	kubectl logs deployment/spark-worker -c spark-worker

open_services:
	minikube addons enable ingress
	kubectl apply -f ./kubernetes/local/minikube-ingress.yaml

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

az_worker:
	kubectl apply -f ./kubernetes/azure/spark-worker-deployment.yaml