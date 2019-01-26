# 5. Minio

For our application we need a place to store pictures.  Object storage is good for this because it is simple and readily available.  S3 is perhaps the most used AWS service because of its availability and cheap price.  For on-prem we can use an open source project called [Minio](https://minio.io/) that not only works on-prem but can configure our cloud based object storage as well such as [S3](https://aws.amazon.com/s3/) and [GCS](https://cloud.google.com/storage/).  

## 5.1 Create a Minio Object Storage System

Creating an instance of Minio with helm is simple. We have, however, added an additional configuration to the service to modify things slightly for our application.  To install this we run:

```
helm install stable/minio --name fonkfe -f https://raw.githubusercontent.com/vallard/K8sServerless/master/minio/config.yaml
```


### 5.1.1 An aside...
If you wanted to customize Minio, you can edit the helm chart config.  You can start by getting the default chart config with:

```
helm inspect values stable/minio >minio-helm-config.yaml
```
You could then change values and update it with:

```
helm upgrade -f minio-helm-config.yaml fonkfe stable/minio
```

##### Challenge 5.1: What did we change from the default configuration?

## 5.2 Verify Minio is up

Ok, let's see if Minio is up:

```
kubectl get pods -l app=minio
```

This returns:

```
fonkfe-544ddf6b86-qpcwf          1/1       Running   0          18m
```
Be sure your pods are `Running` so that things work.

## 5.3 Accessing Minio

Now we want to be able to connect to the front-end from the public Internet (well, we are behind a VPN, but the idea is the same).  In order to do this, there are three ways we could expose our Minio instance.  The first one is to use a LoadBalancer `EXTERNAL-IP`, which is easy. The second way is to use an ingress rule, as we showed in the [Kubernetes Lab](../kubernetes/README.md).  And the third one is to use the Kubernetes cluster IP address and the mapped port for the Minio service. In our helm chart we already configured this to be of type `LoadBalancer` so you should see an `EXTERNAL-IP` already for your instance of Minio.

##### Challenge 5.3: What is the external IP address of Minio?

## 5.4 Log in to Minio browser

To log in we need the access key and the secret key.  These are stored in the Minio secrets file.  You can grab them by examining the `fonkfe` secrets file and base64 decoding the secrets.  However, we have the defaults so we will forgo any decoding exercises for now.  The credentials are:

```
Access Key: AKIAIOSFODNN7EXAMPLE
Secret Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```


Log into Minio with these values at the IP address you found in __challenge 5.3__.  Notice that Minio isn't accessible on port `80`.  How can you find out which port to access Minio?

![minio](../images/minio01.png)

Once logged in you'll see the contents available to you. At this point, there should be nothing!

![minio inside](../images/minio02.png)

## 5.5 Minio Command Line Client

While GUIs are nice, they are also hard for automation tools to interact with.  Let's use the command line client to interact with Minio.

[Download the latest client](https://docs.minio.io/docs/minio-client-complete-guide) for your Operating System

### 5.5.1 Windows

Download the `mc.exe` command and place it in your path.

### 5.5.2 MacOS

Use `homebrew` or download the binary

```
brew install minio/stable/mc
```

## 5.6 Configure and Verify Minio Command line

### 5.6.1 Windows

For Windows it may be easier to just type it out, rather than place it in your path.  Use something like the following command:

![windows mc config](../images/minio03.png)

The access key and secret key should be the same.  The only thing that might be different is the IP address but you should still put the `:9000` at the end:

```
mc config host add minio http://<your minio svc ip>:9000 AKIAIOSFODNN7EXAMPLE wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### 5.6.2 MacOS

Define the environment variables:

```
export MINIO_HOST=http://10.10.20.201:9000
export ACCESS_KEY=AKIAIOSFODNN7EXAMPLE
export SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

Make use of the environment variables to configure Minio.  _Make sure you change the MINIO\_HOST to match your IP address_

```
mc config host add minio $MINIO_HOST $ACCESS_KEY $SECRET_KEY --api S3v4
```

Look at all `mc` hosts:

```
mc config host list
```

Some of these come by default but are not configured (like the `s3` and `gcs`), others like the `play` give you an environment you can mess around in.

## 5.7 Test Minio Upload

Take a picture and save it to your computer desktop, then use Minio to upload the picture.

```
mc mb minio/test
mc cp ~/Desktop/IMG_0952.JPG minio/test/
```

Output will show something uploading:

```
...ktop/IMG_0952.JPG:  2.11 MB / 2.11 MB  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  100.00% 231.74 MB/s 0s
```

Or on Windows:

![mc upload windows](../images/minio04.png)

You should verify that the image was properly placed in the storage bucket in the web interface. 

## 5.8 Conclusion

With Minio up we now have object storage.  While this is a quick way to set it up, this is not good for production.  We would like to be able to make sure that the volumes persist if the container goes down, or even if the host goes down.  We can do this with [persistent volumes (PV)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) and [persistent volume claims (PVC)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims).  In addition we could use more Minio nodes to provide the scale and availability for our cluster.

## Sources

* [https://blog.minio.io/lambda-computing-with-minio-and-kafka-de928897ccdf](https://blog.minio.io/lambda-computing-with-minio-and-kafka-de928897ccdf)
* [https://docs.minio.io/docs/minio-bucket-notification-guide](https://docs.minio.io/docs/minio-bucket-notification-guide)

## Where to next?

* [Go Back Home](../README.md)
* [Previous Module: MongoDB](../mongo/README.md)
* [Next Module: Kubeless](../kubeless/README.md)
