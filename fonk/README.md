# Fonk Guestbook

The idea of FONK-apps is explained best by the below 4 minute video:

[![Fonk Apps](http://img.youtube.com/vi/Xz7_CY25Fog/0.jpg)](https://youtu.be/Xz7_CY25Fog)

# Guestook installation

We already have much of the prerequisites:

* FaaS: Kubeless
* Object Store: Minio
* NoSQL: MongoDB
* K8s: Cisco Container Platform. 

Now if you wish, you can go deploy the guestbook application [as described in the FONK repo](https://github.com/fonk-apps/fonk-examples/tree/master/guestbook)

The Kubeless portion [is described here](https://github.com/fonk-apps/fonk-examples/tree/master/guestbook/faas/kubeless/python). Note: You already did much of the work with updating the python runtime image so you do not need to change that. 
