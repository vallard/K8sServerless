# Helm

Helm is a package manager for kubernetes applications.  Instead of using yaml files we have an easy way to install applications.  

For serverless applications we require an object store and a mongodb database.  We could install these with yaml files and it's not so hard to do that, but helm helps us with rollback and versions, so we will spend a few minutes installing helm.

## Download Helm

Because our lab is a specific version we need to install a specific version of Helm.  In this case we need `2.10.0-rc.3`.  You can download a binary for whichever operating system you have by downloading from this site:

[helm 2.10.0-rc.3](https://github.com/helm/helm/releases/tag/v2.10.0-rc.3)

### MacOS

Copy the binary to `/usr/local/bin` and helm should run right away.  Test with:

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
