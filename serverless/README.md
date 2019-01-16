# Serverless Backend

We will add several backend API calls now.  We have a photobook so the basic application will allow us to add, view or delete photos.  Thats pretty much all we need.  We could continue to use the `kubeless` commands to deploy the different functions but the [serverless framework](https://serverless.com) gives us a better structured way to manage our kubeless functions. This way we can deploy our functions to execute our photobook. 

To install serverless you need to have node installed.  Assuming you do, `cd` into this directory and run:

```
npm install
```

## Configure the `serverless.yaml` file

We want our services to be available through the ingress controller.  To get this IP address we run:

```
kubectl -n ccp get svc nginx-ingress-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```
This gives us something like `10.10.20.207`.  Make note of this.  

Next, take this IP address and put it into the `serverless.yaml` file appending `.xip.io` to the end:

```
...
  hostname: 10.93.140.128.xip.io
...
```

You'll also notice below where it has the `MINIO_HOST`.  This should be set to the minio IP address:

```
  MINIO_HOST: "minio.10.10.20.207.xip.io"
```

Now we can deploy the function

```
sls deploy -f list
```

To see how our service is doing we can run: 

```
sls logs -f list
```



Call the function
```
serverless invoke -f list -l
```
If we want to change something we edit the file, then run:

```
sls deploy function -f list
```


```
serverless remove
```

The function is now accessible from our [ingress controller](https://kubernetes.io/docs/concepts/services-networking/ingress/).

We should be able to hit it with: 

```
curl http://10.93.140.131.xip.io/list
```

