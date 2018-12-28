# Serverless Backend

The front end needs a back end.  We will use serverless as a more structured way to manage our kubeless functions. 

```
npm install
```

```
serverless deploy
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

