# Minio

Our object store can be configured with: 

```
helm install stable/minio --name fonkfe --set service.type=LoadBalancer,persistence.enabled=false
```

Now let us see if it is up: 

```
kubectl get pods,services
```
This returns: 

```
``
NAME                          READY     STATUS    RESTARTS   AGE
pod/fonkfe-5b674d78db-hwzgc   1/1       Running   0          2m

NAME                 TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)          AGE
service/fonkfe       LoadBalancer   10.100.115.131   10.93.140.130   9000:31569/TCP   2m
service/kubernetes   ClusterIP      10.96.0.1        <none>          443/TCP          4d
```

Noting the minio cluster we can now log into it by opening our web browser to ```<loadbalancer IP>:9000```

![img](../images/minio01.png)

To log in we need the secret and access key.

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

These secrets are base64 encoded.  We can decode this with: 

```
echo "secret" | base64 decode
```
e.g:
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

We can log into minio with these values.

### Minio Command Line Client

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
export MINIO_HOST=10.93.140.130
export ACCESS_KEY=AKIAIOSFODNN7EXAMPLE
export SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

Make use of the environment variables to configure minio

```
mc config host add minio http://$MINIO_HOST:9000 $ACCESS_KEY $SECRET_KEY --api S3v4
```

Look at all buckets

```
mc config host list
```


### Test Minio Upload

take a picture and copy picture to your computer desktop, then use minio to upload the picture

```
mc mb minio/test
mc cp ~/Desktop/IMG_0952.JPG minio/test/
...ktop/IMG_0952.JPG:  2.11 MB / 2.11 MB  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  100.00% 231.74 MB/s 0s
```

You should verify that the image was properly placed in the storage bucket in the web interface. 


With Minio up we now have object storage.  While this is a quick way to set it up, this is not good for production.  We would like to be able to make sure that the volumes persist if the container goes down or if even the host goes down.  We can do this with persistent volumes and persistent volume claims.  In addition we could use more minio nodes to provide the scale and availability for our cluster.  
