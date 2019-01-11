# Kubeless


## Installation 

The Kubeless [installation procedure]( ) is well documented.  For convinence and predictability we will use the v1.0.1 release

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
Kubeless deletes the deployment and the service so its a bit cleaner than using kubectl. 

Let's make a function that builds upon our minio configuration and can create a thumbnail image of our image whenever we upload it to minio. 

## Photo Image Resize Function

### Minio Setup

Need to delete minio and start again? 

```
helm del --purge fonkfe
```
Recreate it: 
```
helm install stable/minio --name fonkfe --set service.type=LoadBalancer,persistence.enabled=true
```

Make some buckets to test with. 

```
mc mb minio/uploads
mc mb minio/thumbs
```

Get the current values:

```
helm inspect values stable/minio >config-old
```
Edit `helm-config` and add the following: 




Update the revision

```
helm upgrade -f config-old fonkfe stable/minio
```


Now let's edit the configMap for minio.  There are a few ways we could do this: 

```
kubectl edit cm fonkfe
```

But we will instead use the `helm` way since `helm` is managing `minio`: 

```
helm get values fonkfe > old_values.yaml
```


Find the spot where the `webhook` is defined and change it to look like the below:

```json
"webhook": {
      "1": {
        "enable": false,
        "endpoint": "http://thumb:8080"
      }
    }
```
 
Now save this config and restart the container.  Then check to make sure you see the `webhook` `thumb` defined.

```
mc admin service restart minio
mc admin config get minio
```
Deploy the event to minio

```
mc event add minio/uploads arn:minio:sqs:us-east-1:1:webhook --event put 
Successfully added arn:minio:sqs:us-east-1:1:webhook
```
(You could also filter by suffixes of items but this is difficult if they use JPEG, jpg, Jpeg, etc for extension names.  Without the filter all items trigger a notification. )

```
mc admin info minio
```

Make rules so we can access the secrets with our python script (otherwise it crashes)

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

Finally set minio to call the function whenever something is uploaded to the `/uploads` directory. You should then see it appear in the `/thumbs` directory!


### Exercise:

Change the function to accept .gif, .png, and .jpeg extensions. 

If you need to update the function:

```
kubeless function update thumb -f resize.py
```


To remove the notification: 

```
mc event remove minio/uploads arn:minio:sqs:us-east-1:1:webhook
```


## Sources

* [https://kubeless.io/docs/quick-start/](https://kubeless.io/docs/quick-start/)
* [https://github.com/kubeless/functions/blob/master/incubator/minio-resize/resize.py](https://github.com/kubeless/functions/blob/master/incubator/minio-resize/resize.py)

