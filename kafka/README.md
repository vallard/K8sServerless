# Kafka

## Installation 

```
helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
helm install --name kafka incubator/kafka
```

More configuration could be done by modifying the config.yaml with the helm chart.  


## Test Kafka

We'll make a test pod that has kafka tools installed so we can test them out.  

```
kubectl create -f testclient.yaml
```

Once you have the testclient pod above running, you can list all kafka
topics with:

```
kubectl -n default exec testclient -- /usr/bin/kafka-topics --zookeeper kafka-zookeeper:2181 --list
```

To create a new topic:

```
kubectl -n default exec testclient -- /usr/bin/kafka-topics --zookeeper kafka-zookeeper:2181 --topic test1 --create --partitions 1 --replication-factor 1
```

To listen for messages on a topic:

```
  kubectl -n default exec -ti testclient -- /usr/bin/kafka-console-consumer --bootstrap-server kafka:9092 --topic test1 --from-beginning
```

To stop the listener session above press: `Ctrl+C`

To start an interactive message producer session:

```
  kubectl -n default exec -ti testclient -- /usr/bin/kafka-console-producer --broker-list kafka-headless:9092 --topic test1
```

To create a message in the above session, simply type the message and press "enter"
To end the producer session try: `Ctrl+C`


