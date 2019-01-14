# Kubeless


## Installation 

The Kubeless [installation procedure](https://kubeless.io/docs/quick-start/) is well documented.  We will repost steps here for convinence and predictability and use the v1.0.1 release

```
kubectl create ns kubeless
kubectl create -f https://github.com/kubeless/kubeless/releases/download/v1.0.1/kubeless-v1.0.1.yaml
```

You should see that all of the resources come up

```
kubectl get all -n kubeless
```

This shows the following: 

```
NAME                                               READY     STATUS              RESTARTS   AGE
pod/kubeless-controller-manager-574cf75749-qxdcg   0/3       ContainerCreating   0          1m

NAME                                          DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/kubeless-controller-manager   1         1         1            0           1m

NAME                                                     DESIRED   CURRENT   READY     AGE
replicaset.apps/kubeless-controller-manager-574cf75749   1         1         0         1m
```

## Patching the Python Runtime

Each serverless function runs in a container.  We call this the `runtime` container.  You can see the runtime environments on the [kubeless github page](https://github.com/kubeless/runtimes).  As serverless is new and constantly evolving things change quick.  However this also means that certain features you may want for your apps are not included in the runtimes.  

The features of `CORS` and file uploads are not included.  Fortunately, we can patch this by using our own runtime environment.  

We have already prepared a new runtime environment for this lab.  To use it we have to modify the [ConfigMap](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/) that we just installed with kubeless. To see it run:

```
kubectl get cm -n kubeless
```  

To modify we run:

```
kubectl edit cm -n kubeless kubeless-config
```

This will put us in a vi session.  We will look for the following lines: 

```
"python:2.7", "phase": "installation"}, {"env": {"PYTHONPATH": "$(KUBELESS_INSTALL_VOLUME)/lib/python2.7/site-packages:$(KUBELESS_INSTALL_VOLUME)"},
    "image": "kubeless/python@sha256:34332f4530508a810f491838a924c36ceac0ec7cab487520e2db2b037800ecda",
```
Very carefully replace the python runtime image with: 

```
"python:2.7", "phase": "installation"}, {"env": {"PYTHONPATH": "$(KUBELESS_INSTALL_VOLUME)/lib/python2.7/site-packages:$(KUBELESS_INSTALL_VOLUME)"},
    "image": "vallard/kubeless-pythonf:2.7",
```

Now we will delete the controller pod so that it rereads the configmaps: 

```
kubectl delete pods -n kubeless -l kubeless=controller
```

This should make cors enabled and file uploads possible on our python runtime containers. 

## Install Kubeless Client

### Mac & Linux

```
export RELEASE=v1.0.1
curl -OL https://github.com/kubeless/kubeless/releases/download/$RELEASE/kubeless_$OS-amd64.zip &&   unzip kubeless_$OS-amd64.zip &&   sudo mv bundles/kubeless_$OS-amd64/kubeless /usr/local/bin/
```

### Windows

Download the `kubeless` from the [releases page](https://github.com/kubeless/kubeless/releases/tag/v1.0.1)


## Deploy test function

Following the quickstart guide we can create a simple hello function.  We create a file `function01.py`

```
def hello(event, context):
  print event
  return event['data']

```

Then deploy it with: 

```
kubeless function deploy hello --runtime python2.7 \
                     --from-file function01.py \
                     --handler test.hello
```
You'll then see with `kubectl` that new pod will come up: 

```
kubectl get pods,svc -l function=hello
```

If you see `ErrImagePull` in the status it means the runtime was improperly typed and needs to be changed.  Repeat the steps above and restart the controller and you should see it deploy. 

kubeless deploys a [deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) and a [service](https://kubernetes.io/docs/concepts/services-networking/service/)

This service by default is of type ClusterIP so it can be called internally but not reached externally unless we create an ingress rule or give the service a LoadBalancer. 

We can then call the function by either using a proxy or spin up our own container to run.  Let's use our own container to do it. 

```
kubectl run alp --image=alpine -- sleep 60000
```
This will deploy a `pod alp-xxxxxxxxxx-xxxxx`.  We can log into this pod with: 

```
export AL=$(kubectl get pods | grep alp | awk '{print $1}')
kubectl exec -it $AL /bin/sh
```

This will put you in the pod.  We can now call the service within this pod since we have access to `ClusterIP`s in the pod space: 

```
apk add --no-cache curl  # install curl
curl -L --data '{"Another": "Echo"}' \
  --header "Content-Type:application/json" \
  hello:8080 
```

This will return exactly what you gave it: 

```
{"Another": "Echo"}
```

Our first function as a service works!

Notice that the way we call other functions or services in kubernetes follows the form: 

```
<svc>.<namespace>.svc.<cluster domain>
```

In this case it was 

```
hello.default.svc.cluster.local
```
By default we are in the same namespace and so we could leave everything else off and just use `hello`. 

## Delete Sample Function

Exit out of the container and delete the hello function

```
exit
kubeless function delete hello
```
Kubeless deletes the deployment and the service so its a bit cleaner than using kubectl to remove everything.


## Photo Image Resize Function

Let's make a function that builds upon our minio configuration and can create a thumbnail image of our image whenever we upload it to minio.  The `event` in this case is a file upload.  This will trigger a call to our photo resize function.  

### Make Buckets

We will use this function in our big application.  Let's make some buckets first:

```
mc mb minio/uploads
mc mb minio/thumbs
```

### Make Webhooks
 
You can add `webhooks` minio.  We already added these with the config file you used to create the helm chart in the beginning.  Run the command:  

```
mc admin config get minio
```

You will see an entry: 

```json
"webhook": {
			"1": {
				"enable": true,
				"endpoint": "http://thumb:8080"
			}
		}
```

This is the first webhook `1` that is available to us.  Let's use it: 

```
mc event add minio/uploads arn:minio:sqs:us-east-1:1:webhook --event put 
```

(You could also filter by suffixes of items but this is difficult if they use JPEG, jpg, Jpeg, etc for extension names.  Without the filter all items trigger a notification. ).  We can now see the webhook is ready:

```
mc admin info minio
```

Make rules so we can access the secrets with our python script (otherwise it crashes).  This is insecure!  However, we will use it just to make it work for now:

```
kubectl create clusterrolebinding default-cluster-admin --clusterrole=cluster-admin --serviceaccount=default:default
```


Now we add our function:

```
kubeless function deploy thumb \
 --runtime python2.7 \
 --handler resize.thumbnail \
 --from-file resize.py \
 --dependencies requirements.txt
```

Now upload an image in the `uploads` bucket but be sure the extension is `JPEG`.  You should instantly see a smaller version appear in the `/thumbs` directory!


### Exercise:

Change the function to accept .gif, .png, and .jpeg extensions. 

If you need to update the function:

```
kubeless function update thumb -f resize.py
```


##### (optional, but don't do it) To remove the notification you would run:

```
mc event remove minio/uploads arn:minio:sqs:us-east-1:1:webhook
```



## Sources

* [https://kubeless.io/docs/quick-start/](https://kubeless.io/docs/quick-start/)
* [https://github.com/kubeless/functions/blob/master/incubator/minio-resize/resize.py](https://github.com/kubeless/functions/blob/master/incubator/minio-resize/resize.py)

