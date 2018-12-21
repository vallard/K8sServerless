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

### Testing a basic Serverless Application

* [FONK Guestbook](fonk/)

### Building a more complex serverless Application

* [NodeJS Frontend](photos/)
* [FaaS Backend](faas/)
* [Security Revisions](security/)

## Credits and Shoutouts

Much of the work here is based off the FONK idea that Pete Johnson has been pushing.  Julio also has made large contributions by speaking and adding code to this terrific movement. We are hopeful that as we go forward more people find the ideas of serverless bring great promise to on prem workloads and are not limited to public clouds only. 

* [Pete Johnson](https://twitter.com/nerdguru)
* [Julio Gomez](https://twitter.com/juliodevops)

