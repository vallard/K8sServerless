# On Prem Serverless

[Serverless Architectures](https://www.martinfowler.com/articles/serverless.html) are becoming quite popular with developers.  They allow you to write less code and do rapid prototypes faster.  

You usually hear about serverless in the public clouds such as AWS, Google, and Microsoft.  But thanks to Kubernetes we can also run serverless on prem using the [serverless framework](https://serverless.com) with several different kubernetes serverless integrations.  

In this lab we will create a serverless application ontop of an on-prem kubernetes. The basis of this work is from Pete Johnson's [Fonk Apps](https://fonk-apps.io) project.

## Part I: Building the Platform

* [DEVNET Sandbox](sb/)
* [CCP Kubernetes](kubernetes/)
* [Helm](helm/)
* [Minio](minio/)
* [MongoDB](mongo/)
* [Kubeless](kubeless/)

## Part II: Building a Serverless Application

* [FONK Guestbook](fonk/)
* [NodeJS Frontend](node/)
* [FaaS](faas/)
* [Security Revisions](security/)

## Credits and Shoutouts

* [Julio Gomez](https://twitter.com/juliodevops)
* [Pete Johnson](https://twitter.com/nerdguru)
