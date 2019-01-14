# Mongo DB

## Install MongoDB

We can use the helm chart again with the following:

```
helm install stable/mongodb --name fonkdb 
```

This may take a while to return and will give you output including how to connect to the database:

```
** Please be patient while the chart is being deployed **

MongoDB can be accessed via port 27017 on the following DNS name from within your cluster:

    fonkdb-mongodb.default.svc.cluster.local

To get the root password run:

    export MONGODB_ROOT_PASSWORD=$(kubectl get secret --namespace default fonkdb-mongodb -o jsonpath="{.data.mongodb-root-password}" | base64 --decode)

To connect to your database run the following command:

    kubectl run --namespace default fonkdb-mongodb-client --rm --tty -i --restart='Never' --image bitnami/mongodb --command -- mongo admin --host fonkdb-mongodb --authenticationDatabase admin -u root -p $MONGODB_ROOT_PASSWORD

To connect to your database from outside the cluster execute the following commands:

    kubectl port-forward --namespace default svc/fonkdb-mongodb 27017:27017 &
    mongo --host 127.0.0.1 --authenticationDatabase admin -p $MONGODB_ROOT_PASSWORD
```

We can make sure our mongo database is up with:

```
kubectl get pods,services -l app=mongodb
```

The output is:

```
NAME                                 READY     STATUS              RESTARTS   AGE
pod/fonkdb-mongodb-c474fff64-r54tz   0/1       ContainerCreating   0          2m

NAME                     TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)           AGE
service/fonkdb-mongodb   LoadBalancer   10.107.150.119   10.93.140.132   27017:30943/TCP   2m
```

Make sure that the container is in `RUNNING` state.  We should now have access to our database!  

To delete this we could run `helm delete --purge fonkdb`

## Testing MongoDB

In this section we will explore some of the ways MongoDB works and how we can do quieries. 

```
export MONGODB_ROOT_PASSWORD=$(kubectl get secret --namespace default fonkdb-mongodb -o jsonpath="{.data.mongodb-root-password}" | base64 --decode)
```

The password for `sls` is:

```
export MONGODB_PASSWORD=$(kubectl get secret --namespace default fonkdb-mongodb -o jsonpath="{.data.mongodb-password}" | base64 --decode)
```

Now we can connect with: 

```
kubectl run --namespace default fonkdb-mongodb-client --rm --tty -i --restart='Never' --image bitnami/mongodb --command -- mongo admin --host fonkdb-mongodb --authenticationDatabase admin -u root -p $MONGODB_ROOT_PASSWORD
```
This will put us at the mongo db console to run some commands. 

You'l see a command prompt:

```
>
```

MongoDB is a document database.  We can read, add, and change information in the document.  We don't need any structure.  For example, let's suppose we had a bunch of fashionable bags we were selling.  We could create a document that had 1 hand bag:

```json
{
	"brand" : "versace",
	"description": "small quilted icon shoulder bag",
	"quantity": 40	
}
```

First let's create our store:

```
> use Inventory
```

This will create our database if it wasn't created already.  Now let's create a collection, or a table.  This will be a collection of documents or records in this database.  T

```
db.Inventory.insert( { "brand" : "Versace", "description": "small quilted icon shoulder bag", "quantity" : 40 } )
```
We will get back the output: 

```
WriteResult({ "nInserted" : 1 })
```

Now let's read from the database: 

```
db.Inventory.find().forEach(printjson)
```
This will print out the entry that we created.  But we'll see that it added a field:

```
{
	"_id" : ObjectId("5c3ccc7f019828cae0088609"),
	"brand" : "Versace",
	"description" : "small quilted icon shoulder bag",
	"quantity" : 40
}
```
An `_id` field of `ObjectId`.  Now let's suppose that someone bought one of these types of bags.  We would need to decrement the quantity.  To do this, we need to modify the record.  We can use the `_id` field to update the record:

```
db.Inventory.update({"_id" : ObjectId("5c3ccc7f019828cae0088609")},
... {$set: {"quantity" : 39 }});
```
Notice that in this instance I used the ObjectID that was assigned to the record I used.  You will need to use the `ObjectId` that was automatically created for your entry.  

Reading it back, we can see that it is now quantity `39`.  

```
db.Inventory.find().forEach(printjson)
```

The power of using unstructured data is that we can now add a field to our object.  Let's suppose that we want to add a field that shows the color of this item. 

```
db.Inventory.update({"_id" : ObjectId("5c3ccc7f019828cae0088609")}, {$set: {"color" : "white" }});
```
In structured SQL we would have to add another column.  In NoSQL we can simply add the field when we want.  Each object might look different.  This can be inherently messy but can help us quickly iterate through our design of our application.  

```
> db.Inventory.find().forEach(printjson)
{
	"_id" : ObjectId("5c3ccc7f019828cae0088609"),
	"brand" : "Versace",
	"description" : "small quilted icon shoulder bag",
	"quantity" : 39,
	"color" : "white"
}
```


Finally, we can remove this object from the database: 

```
db.Inventory.remove({"_id" : ObjectId("5c3ccc7f019828cae0088609")})
```


## Sources

* [Mongo CRUD Operations](https://docs.mongodb.com/manual/crud/)
* [Mongo Guru99 Tutorial](https://www.guru99.com/mongodb-query-document-using-find.html)




