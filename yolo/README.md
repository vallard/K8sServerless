# Object Recognition

Object Recognition in photos has made many advances in the last several years.  The advances have come from more data, better algorithms, and better more computing power. 

## YOLO

[YOLO](https://pjreddie.com/darknet/yolo/) is a real time object detection algorithm with a [flexible license](https://github.com/pjreddie/darknet/blob/master/LICENSE.fuck).  Like many machine learning algorithms it is open source and we are able to use it in many different applications free of charge. 

![img](https://pjreddie.com/media/image/Screen_Shot_2018-03-24_at_10.48.42_PM.png)
(source: [YOLO homepage](https://pjreddie.com/darknet/yolo/))

We will take an implementation of this algorithm that has already been trained and use that model to do object recognition inside our photos that we upload.  We will then tag the data in our photos with the objects that the algorithm recognizes.

## Install YOLO Detector

I have made a small application for you called [YOLO Detector](https://github.com/vallard/YOLO-Detector).  It embeds the YOLO algorithm and model in a Tensorflow implementation and does the image detection for you.  Because it is small it doesn't recognize many things.  It can do: 


* aeroplane
* bicycle
* bird
* boat
* bottle
* bus
* car
* cat
* chair
* cow
* diningtable
* dog
* horse
* motorbike
* person
* pottedplant
* sheep
* sofa
* train
* tvmonitor

So don't expect too much!  

Let's install it by running:

```
kubectl apply -f https://raw.githubusercontent.com/vallard/YOLO-Detector/master/manifests/yolo-detector.yaml
```
This will create a deployment and a service in Kubernetes called `yolo`.  It may take a while to pull as the image is about 2GB.  This is because the model is big. 



## Hooking Things up

We have a service that can be called.  But how do we hook it up to the rest of the environment?  

Currently it stands alone as a seperate service.  We could have it be called as another webhook similar to how the image is called.  But why not go for scale here and instead use kafka?  That way we can create a pubsub mechanism to deal with scale.  

## Kafka

```
helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
helm install --name my-kafka incubator/kafka
```  

Now we can use it.

```


```
You can connect to Kafka by running a simple pod in the K8s cluster like this with a configuration like this:

  apiVersion: v1
  kind: Pod
  metadata:
    name: testclient
    namespace: default
  spec:
    containers:
    - name: kafka
      image: confluentinc/cp-kafka:5.0.1
      command:
        - sh
        - -c
        - "exec tail -f /dev/null"

Once you have the testclient pod above running, you can list all kafka
topics with:

  kubectl -n default exec testclient -- /usr/bin/kafka-topics --zookeeper my-kafka-zookeeper:2181 --list

To create a new topic:

  kubectl -n default exec testclient -- /usr/bin/kafka-topics --zookeeper my-kafka-zookeeper:2181 --topic test1 --create --partitions 1 --replication-factor 1

To listen for messages on a topic:

  kubectl -n default exec -ti testclient -- /usr/bin/kafka-console-consumer --bootstrap-server my-kafka:9092 --topic test1 --from-beginning

To stop the listener session above press: Ctrl+C

To start an interactive message producer session:
  kubectl -n default exec -ti testclient -- /usr/bin/kafka-console-producer --broker-list my-kafka-headless:9092 --topic test1

To create a message in the above session, simply type the message and press "enter"
To end the producer session try: Ctrl+C


```

Turn minio into a kafka producer.  It writes on the `uploads` topic.  Run the command:

```
mc event add minio/uploads arn:minio:sqs:us-east-1:1:kafka --event put
```

Now we need to have our function trigger when topics are pushed

```
kubeless function deploy test --runtime python2.7 \
                                --handler test.foobar \
                                --from-file test.py
```



```
kubeless trigger kafka create test --function-selector created-by=kubeless,function=test --trigger-topic test-topic
```


## Reference

[https://kubeless.io/docs/pubsub-functions/#kafka](https://kubeless.io/docs/pubsub-functions/#kafka)
