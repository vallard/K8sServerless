# 3. Helm

Helm is a package manager for kubernetes applications.  Instead of using yaml files we have an easy way to install applications.  The benefit comes when applications are comprised of multiple pods and/or services.  Helm calls these bundles [charts](https://github.com/helm/charts)

For serverless applications we require an object store and a mongodb database.  We could install these with yaml files and it's not so hard to do that, but helm helps us with rollback and versions, so we will spend a few minutes installing helm.

## 3.1 Download Helm

Because our lab is a specific version we need to install a specific version of Helm.  In this case we need `2.10.0`.  You can download a binary for whichever operating system you have by downloading from this site:

[helm 2.10.0](https://github.com/helm/helm/releases/tag/v2.10.0)

(scroll down past the `What's Changed` section to see the binary downloads)

### 3.1.1 Windows

Download the windows binary and put it in your path.  

### 3.1.2 MacOS

Copy the binary to `/usr/local/bin` and helm should run right away.  Test with:

```
cd ~/Downloads
tar zxvf helm-v2.10.0-darwin-amd64.tar.gz
mv darwin-amd64/helm /usr/local/bin
```

### 3.1.3 Validate Helm

```
helm list
```
This should show you that some of the default CCP packages are installed with helm:

```
NAME                	REVISION	UPDATED                 	STATUS  	CHART                     	APP VERSION	NAMESPACE
ccp-efk             	1       	Sun Jan 13 21:10:37 2019	DEPLOYED	ccp-efk-0.1.0             	           	ccp
ccp-monitor         	1       	Sun Jan 13 21:10:35 2019	DEPLOYED	ccp-monitor-0.1.0         	           	ccp
kubernetes-dashboard	1       	Sun Jan 13 21:10:34 2019	DEPLOYED	kubernetes-dashboard-0.7.1	1.8.3      	ccp
metallb             	1       	Sun Jan 13 21:10:33 2019	DEPLOYED	metallb-0.4.0             	0.6.2      	ccp
nginx-ingress       	1       	Sun Jan 13 21:10:32 2019	DEPLOYED	nginx-ingress-0.24.0      	0.17.1     	ccp
```

Wasn't that easy? You are doing very well in this course!

## Where to next?

* [Go Back Home](../README.md)
* [Previous Module: CCP Kubernetes](../kubernetes/README.md)
* [Next Module: MongoDB](../mongo/README.md)
