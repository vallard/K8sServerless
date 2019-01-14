# Serverless Backend

The front end needs a back end.  We will use serverless as a more structured way to manage our kubeless functions. This way we can deploy our functions to execute our photobook. 

To install serverless you need to have node installed.  Assuming you do, `cd` into this directory and run:

```
npm install
```

## Configure the `serverless.yaml` file

We want our services to be available through the ingress controller.  We can use: 

```
kubectl get svc nginx-ingress-controller -n ccp
```
In the output (similar to what is shown below, you will see the `EXTERNAL-IP`

```
NAME                       TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)                      AGE
nginx-ingress-controller   LoadBalancer   10.101.176.99   10.93.140.128  80:30848/TCP,443:31459/TCP   28d
```
Take this IP address and put it into the `serverless.yaml` file appending `.xip.io` to the end:

```
...
  hostname: 10.93.140.128.xip.io
...
```

Now we can deploy the function

```
serverless deploy function -f list
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

