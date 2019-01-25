# 8. Serverless Back-end

We will add several back-end API calls now.  We have a photobook, so the basic application will allow us to add, view or delete photos.  That's pretty much all we need.  We could continue to use the `kubeless` commands to deploy the different functions but the [serverless framework](https://serverless.com) gives us a better structured way to manage our Kubeless functions. This way we can deploy our functions to execute our photobook.

## 8.1 Install node

Because the serverless framework is written in JavaScript, you will need to install [Node and npm](https://www.npmjs.com/get-npm).  

### 8.1.1 Windows

1. [Get installer](https://nodejs.org/en/download/).
2. Install packages.
3. Run `node -v` on command line to verify.

### 8.1.2 MacOS

1. [Get installer](https://nodejs.org/en/download/).
2. Install packages.
3. Run `node -v` on command line to verify.

## 8.2 Install serverless

```
npm install -g serverless
```

If all goes well you will have the serverless platform installed in your workstation.  

## 8.3 Get code

We now need to get the code from GitHub, in order to build our system.  So first you will need to install [Git](https://git-scm.com/) in your system.

### 8.3.1 Git for Windows

[Download code](https://git-scm.com/download/win).

### 8.3.2 Git for MacOS

You can use `brew` or grab from [here](https://git-scm.com/downloads).

### 8.3.3 Download this repository

On the command line go to a directory where you will remember (I use `~/Code` for all my code, but feel free to customize as you desire),

From there, run:

```
git clone https://github.com/vallard/K8sServerless.git
```

This will download the entire repository you are currently reading.  

## 8.4 Deploy Serverless Functions

### 8.4.1 Install package dependencies

There are package dependencies that need to be installed for the serverless-kubeless plugin.  

You can examine the package dependencies in the `./K8sServerless/serverless/package.json` file.  

To install the dependencies do the following:

```
cd <repos-dir>/K8sServerless/serverless
npm install
```

### 8.4.2 Configure the `serverless.yaml` file

We want our services to be available through the ingress controller.  To get this IP address we run:

```
kubectl -n ccp get svc nginx-ingress-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```
This gives us something like `10.10.20.200`.  Make note of this.  

Next, take this IP address and put it into the `serverless.yaml` file appending `.xip.io` to the end:

```
...
  hostname: 10.10.20.200.xip.io
...
```

You'll also notice several places where `MINIO_HOST` is defined.  This should be set to the Minio service IP address.  (Remember: Minio is named `fonkfe` in our helm deployment, so getting the Kubernetes service `EXTERNAL-IP` address for this is what you are looking for)

```
  MINIO_HOST: "10.10.20.201:9000"
```

### 8.4.3 Deploy the serverless functions

Deploy the functions:

```
sls deploy
```

Output (it might take some minutes):

```
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Deploying function delete...
Serverless: Deploying function list...
Serverless: Deploying function upload...
Serverless: Function list successfully deployed
Serverless: Function upload successfully deployed
Serverless: Function delete successfully deployed
```

If you get some errors, try running `sls deploy` again.

## 8.5 Test/Verify Serverless Functions

To see how our service is doing we can run:

```
sls logs -f list
```

Call the function:

```
sls invoke -f list -l
```

Output:

```
{"photos": []}
```

The function is now accessible from our [ingress controller](https://kubernetes.io/docs/concepts/services-networking/ingress/).  You can see the ingress rules created by running:

```
kubectl get ing
```

You'll see a newly created `photos` ingress rule, alongside your old rule:

```
NAME      HOSTS                      ADDRESS                     PORTS     AGE
ngx1      ngx1.10.10.20.200.xip.io   10.10.20.113,10.10.20.114   80        20h
photos    10.10.20.200.xip.io        10.10.20.113,10.10.20.114   80        8m
```

We should be able to hit it with:

```
curl http://<your ingress controller host>.xip.io/images/list
```

If you get:

```
default backend - 404
```

... then something is not right.  Check your work, ask for help, and fix it before moving on.  

## 8.6 Challenge: Modify code

Take a look at the `photos.py` file.  You'll notice there is a function called `upload(event, context)`.  Modify the record that gets inserted into the database by adding a timestamp.  Call the entry `date`.  You may find the `datetime.datetime.utcnow()` function helpful.

As you can see testing in a serverless environment is not always trivial.  This presents one of the drawbacks of this method of developing.

There are a few troubleshooting commands that can help you:

```
kubectl get pods
kubectl logs -f <podname>
kubectl describe ing photos
```

Python errors will prevent the container from starting.  The logs would show you where that is.


## 8.7 Serverless Conclusion

At this point three serverless functions have been installed to allow us to upload photos, list them, and delete them.

## Where to next?

* [Go Back Home](../README.md)
* [Previous Module: Application Overview](../photos/OVERVIEW.md)
* [Next Module: Front-end time!](../photos/README.md)
