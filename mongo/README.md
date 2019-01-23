# 4. Mongo DB

## 4.1 Install MongoDB

Now that we have helm let's put it to the test and install a mongo db database.  But wait! you say, installing a database is hard work!  Well let's just see about that!  Run the command:

```
helm install stable/mongodb --name fonkdb 
```

And just like that you created a mongodb database suitable for our application needs. It even gives you a few notes at the end as to how to connect to it.  Let's do this now to explore how to use a no-sql database. 

## 4.2 Verify MongoDB is operational
 

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

You'll notice that the database `svc` is not given an `EXTERNAL-IP`.  This is not something we want to change.  The database sits in the background and we want as much protection around it as possible. 

## 4.3 Testing MongoDB

In this section we will explore some of the ways MongoDB works and perform some operations.  But if we can't connect to it with our laptops, how can we connect and perform operations?  Kubernetes has the answer for us again. 


### 4.3.1 Connect to MongoDB

Let's first get the password so we can login.  

```
export MONGODB_ROOT_PASSWORD=$(kubectl get secret --namespace default fonkdb-mongodb -o jsonpath="{.data.mongodb-root-password}" | base64 --decode)
```

Now we can connect with: 

```
kubectl run --namespace default fonkdb-mongodb-client --rm --tty -i --image bitnami/mongodb --command -- mongo admin --host fonkdb-mongodb --authenticationDatabase admin -u root -p $MONGODB_ROOT_PASSWORD
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
### 4.3.2 Create Resources in MongoDB

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
An `_id` field of `ObjectId`.  What is this?  

MongoDB ads a unique field for every document entered.  If you don't specify one (which you can) then Mongo creates its own.  It is of type [ObjectId](https://docs.mongodb.com/manual/reference/method/ObjectId/).  In this way it can reference every document uniquely.  

### 4.3.3 Updating A document

Now let's suppose that someone bought one of these types of bags.  We would need to decrement the quantity.  To do this, we need to modify the record.  We can use the `_id` field to update the record.  

```
db.Inventory.update({"_id" : ObjectId("<YOUR OBJECT ID>")},
   {$set: {"quantity" : 39 }});
```
Notice that in this instance I used the ObjectID that was assigned to the record I used.  You will need to use the `ObjectId` that was automatically created for your entry.  

Reading it back, we can see that it is now quantity `39`.  

```
db.Inventory.find().forEach(printjson)
```

The power of using unstructured data is that we can now add a field to our object.  Let's suppose that we want to add a field that shows the color of this item. (Again put in your object ID for this command)

```
db.Inventory.update({"_id" : ObjectId("<YOUR OBJECT ID>")}, {$set: {"color" : "white" }});
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

### 4.3.4 Removing items

Finally, we can remove this object from the database: 

```
db.Inventory.remove({"_id" : ObjectId("<YOUR OBJECT ID>")})
```

When it comes down to it, all we are doing with applications are updating and modifying databases. 


## Sources

* [Mongo CRUD Operations](https://docs.mongodb.com/manual/crud/)
* [Mongo Guru99 Tutorial](https://www.guru99.com/mongodb-query-document-using-find.html)

## Where to next?

* [Go Back Home](../README.md)
* [Previous Module: Where in the Helm?](../helm/README.md)
* [Next Module: Minio](../minio/README.md)



