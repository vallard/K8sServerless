# Object Recognition

Object Recognition in photos has made many advances in the last several years.  The advances have come from more data, better algorithms, and mountains of cheap computing power. 

## YOLO

[YOLO](https://pjreddie.com/darknet/yolo/) is a real time object detection algorithm with a [flexible license](https://github.com/pjreddie/darknet/blob/master/LICENSE.fuck).  Like many machine learning algorithms it is open source and we are able to use it in many different applications free of charge. 

![img](https://pjreddie.com/media/image/Screen_Shot_2018-03-24_at_10.48.42_PM.png)
(source: [YOLO homepage](https://pjreddie.com/darknet/yolo/))

We will take an implementation of this algorithm that has already been trained and use that model to do object recognition inside our photos that we upload.  We will then tag the data in our photos with the objects that the algorithm recognizes.

## Install YOLO Detector

I have made a small application for you called [YOLO Detector](https://github.com/vallard/YOLO-Detector).  It embeds the YOLO algorithm and model in a Tensorflow implementation and does the image detection for you.  Because the model is (relatively) small it doesn't recognize many things.  It can detect the following objects:

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

We have a service but we need an event mechanism to invoke the function.  How can we hook it up to the application? 

Currently it stands alone as a seperate service.  We could have it be called as another webhook similar to how the image is called.  But why not go for scale here and instead use kafka?  That way we can create a pubsub mechanism to deal with scale. 

![img](../images/yolo01.png) 

## Kafka

We could install kafka using helm or other ways but we will use the sample kubeless version as it hooks everything up for us. 

### Install kafka and kubeless kafka plugin

```
export RELEASE=$(curl -s https://api.github.com/repos/kubeless/kafka-trigger/releases/latest | grep tag_name | cut -d '"' -f 4)
kubectl create -f https://github.com/kubeless/kafka-trigger/releases/download/$RELEASE/kafka-zookeeper-$RELEASE.yaml
```
Now we can use it.

```
kubectl create -f https://raw.githubusercontent.com/vallard/K8sServerless/master/yolo/kafka-testclient.yaml
```

### Test kafka installation 

We can now list the different topics within it:

```
  kubectl -n default exec testclient -- /usr/bin/kafka-topics --zookeeper zoo.kubeless:2181 --list
```

Now we can listen for messages on the topic.  In this case 

To create the `uploads` topic if it hasn't been created:

```
  kubectl -n default exec testclient -- /usr/bin/kafka-topics --zookeeper zoo.kubeless:2181 --topic uploads --create --partitions 1 --replication-factor 1
```

Now we will listen to the messages on this topic

```
  kubectl -n default exec -it testclient -- /usr/bin/kafka-console-consumer --bootstrap-server kafka.kubeless:9092 --topic uploads --from-beginning
```

Now when you upload a new image using the app you'll see an event name:

```json
{"EventName":"s3:ObjectCreated:Put","Key":"uploads/Fortnite-Small.png","Records":[{"eventVersion":"2.0","eventSource":"minio:s3","awsRegion":"us-east-1","eventTime":"2019-01-16T06:28:20Z","eventName":"s3:ObjectCreated:Put","userIdentity":{"principalId":"AKIAIOSFODNN7EXAMPLE"},"requestParameters":{"accessKey":"AKIAIOSFODNN7EXAMPLE","region":"us-east-1","sourceIPAddress":"10.10.20.116"},"responseElements":{"x-amz-request-id":"157A40482507E473","x-minio-origin-endpoint":"http://127.0.0.1:9000"},"s3":{"s3SchemaVersion":"1.0","configurationId":"Config","bucket":{"name":"uploads","ownerIdentity":{"principalId":"AKIAIOSFODNN7EXAMPLE"},"arn":"arn:aws:s3:::uploads"},"object":{"key":"Fortnite-Small.png","size":223865,"eTag":"dae67bfdbc2778805c9ee4daee42aadd","contentType":"image/png","userMetadata":{"content-type":"image/png"},"versionId":"1","sequencer":"157A4048256B4083"}},"source":{"host":"","port":"","userAgent":"Minio (Linux; x86_64) minio-py/4.0.9"}}]}
```
To stop the listener session above press: `Ctrl+C`

## Minio as a Kafka Producer

Next we need to turn minio into a kafka producer.  We want a message to be emitted when photos are uploaded to the `uploads` topic.  Run the command:

```
mc event add minio/uploads arn:minio:sqs:us-east-1:1:kafka --event put
```

## Add Kubeless Function for processing Images

Next let's create a function that can be called as messages come in from kafka.  To do this we run: 

```
kubeless function deploy rek --runtime python2.7 \
                    --handler rek.process_event \
                    --dependencies requirements.txt \
                    --from-file rek.py
```

## Add Kubeless Trigger
Finally we need to tie the kafka trigger to the function: 


```
kubeless trigger kafka create rek --function-selector created-by=kubeless,function=rek --trigger-topic uploads
```

Now you should be able to upload an image.  Then after waiting a bit if you refresh the page you will see that it tries to recognize the objects it sees in the page.

![img](../images/yolo02.png)

In the above picture we see that it recognized 10 different people with different degrees of certainty.  

__Note:__ You have to upload a new picture as the event is only triggered on new uploads.  Previous uploads won't do anything.  

## Exercise

To update the function:

```
kubeless function update rek -f rek.py
```


## Reference

[https://kubeless.io/docs/pubsub-functions/#kafka](https://kubeless.io/docs/pubsub-functions/#kafka)
