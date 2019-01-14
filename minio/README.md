# Minio

Our object store can be configured with: 

```
helm install stable/minio --name fonkfe -f https://
```

Now let us see if it is up: 

```
kubectl get pods
```

This returns: 

```
...
fonkfe-544ddf6b86-qpcwf          1/1       Running   0          18m
...
```
Be sure your pods are `Running` so that things work. 

## Accessing Minio

Now we want to be able to connect to the frontend from the public Internet.  (Well we are behind a VPN, but the idea is the same).  In order to do this there are two ways we could expose our minio instance.  The first is to use a LoadBalancer `EXTERNAL-IP` which is easy, the second is to use an ingress rule.

### (option 1) LoadBalancer

We edit the service by adding the `LoadBalancer` field to it.  

```
kubectl edit svc fonkfe
```
Where you will see:

```
...
  type: ClusterIP
...
```
Change it to be:

```
  type: LoadBalancer
```

Write changes and save. An IP address will be assigned.  View it with `kubectl get svc fonkfe`.  You can enter this IP address in the browser, along with the port `9000` to get on to the minio dashboard. 

e.g: `http://10.10.20.208:9000`


### (option 2) Access With Ingress

CCP already comes with an [ingress controller](https://kubernetes.io/docs/concepts/services-networking/ingress/) installed.  To use it we just need to make a rule. 

First let's get the IP address of the ingress controller:

```
kubectl -n ccp get svc nginx-ingress-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}
```
This should give you out an IP address such as `10.10.20.207`.  Make note of this IP address.  

We will use the [xip](http://xip.io/) service and a Kubernetes ingress rule so that if we point our browsers to [https://minio.10.10.20.207.xip.io](https://minio.10.10.20.207.xip.io) then it will go straight to minio. 
 
An ingress rule is pretty simple.  We specify the name of the service, the route, and the DNS name we expect.  You can download the ingress rule at the main source site. 

#### Download Ingress Rule

```
wget https://raw.githubusercontent.com/vallard/K8sServerless/master/minio/minio-ing.yaml
```

Open this file with your favorite editor and change the host entry from `minio.10.10.20.207.xip.io` to your host ingress controller IP address that you copied from above. 

Deploy the ingress controller with: 

```
kubect create -f minio-ing.yaml
```

Now you should be able to open a browser to the minio web page.

![img](../images/minio01.png)

## Log in to minio

To log in we need the access key and the secret key.  These are stored in the minio secrets file.  You can grab them as follows: 

```
kubectl get secret fonkfe -o yaml
```

Here we get the output similar to as follows:

```yaml
apiVersion: v1
data:
  accesskey: QUtJQUlPU0ZPRE5ON0VYQU1QTEU=
  secretkey: d0phbHJYVXRuRkVNSS9LN01ERU5HL2JQeFJmaUNZRVhBTVBMRUtFWQ==
kind: Secret
metadata:
  creationTimestamp: 2018-12-18T23:43:44Z
  labels:
    app: minio
    chart: minio-2.2.0
    heritage: Tiller
    release: fonkfe
  name: fonkfe
  namespace: default
  resourceVersion: "816207"
  selfLink: /api/v1/namespaces/default/secrets/fonkfe
  uid: c193e532-031e-11e9-906a-005056a52355
type: Opaque
```

These secrets are base64 encoded.  They are:

```
Access Key: AKIAIOSFODNN7EXAMPLE 
Secret Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

Use these to log into your minio dashboard.  For information, you can get these keys to be not base64 encoded by decoding them.  Decoding them is done like so: 

```
echo "secret" | base64 decode
```
e.g. in the above: 

```
echo QUtJQUlPU0ZPRE5ON0VYQU1QTEU= | base64 --decode
```
Which gives us the output of: 

```
AKIAIOSFODNN7EXAMPLE
```

Similarly we need to get the secret decoded of the `secretkey`

```
echo d0phbHJYVXRuRkVNSS9LN01ERU5HL2JQeFJmaUNZRVhBTVBMRUtFWQ== | base64 --decode
```

Which gives us the output of:

```
wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

Log into minio with these values.

### Minio Command Line Client

While GUI's are nice they are hard to right automation tools against.  Let's use the command line client to interact with minio. 

[Download the latest client](https://docs.minio.io/docs/minio-client-complete-guide) for your Operating System

#### Windows

Download the `mc.exe` command 

#### Mac

Use homebrew or download the binary

```
brew install minio/stable/mc
```

### Configure Minio Command line

Define the environment variables

```
export MINIO_HOST=http://minio.10.10.20.207.xip.io
export ACCESS_KEY=AKIAIOSFODNN7EXAMPLE
export SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

Make use of the environment variables to configure minio.  _Make sure you change the MINIO\_HOST to match your IP address_

```
mc config host add minio $MINIO_HOST $ACCESS_KEY $SECRET_KEY --api S3v4
```

Look at all buckets

```
mc config host list
```
Some of these come by default but are not configured (like the `s3` and `gcs`), others like the `play` give you an environment you can mess around in.


### Test Minio Upload

take a picture and copy picture to your computer desktop, then use minio to upload the picture

```
mc mb minio/test
mc policy 
mc cp ~/Desktop/IMG_0952.JPG minio/test/
```

Output will show something uploading:
 
```
...ktop/IMG_0952.JPG:  2.11 MB / 2.11 MB  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  100.00% 231.74 MB/s 0s
```

You should verify that the image was properly placed in the storage bucket in the web interface. 


With Minio up we now have object storage.  While this is a quick way to set it up, this is not good for production.  We would like to be able to make sure that the volumes persist if the container goes down or if even the host goes down.  We can do this with persistent volumes and persistent volume claims.  In addition we could use more minio nodes to provide the scale and availability for our cluster.



## Sources

* [https://blog.minio.io/lambda-computing-with-minio-and-kafka-de928897ccdf](https://blog.minio.io/lambda-computing-with-minio-and-kafka-de928897ccdf)
* [https://docs.minio.io/docs/minio-bucket-notification-guide](https://docs.minio.io/docs/minio-bucket-notification-guide)