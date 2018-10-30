# IBM Cloud SQL Database
This tutorial shows how to provision a SQL (relational) database service, create a table and load a larger data set, city information into the database. Thereafter, we deploy a web app "worldcities" to make use of that data and show how to access the cloud database. The app is written in Python using the [Flask framework](http://flask.pocoo.org/).

This tutorial is part of [IBM Cloud tutorials](https://console.bluemix.net/docs/tutorials/index.html) and discussed as [SQL Database for Cloud Data](https://console.bluemix.net/docs/tutorials/sql-database.html).

# Up and running in few steps
To get this SQL database-backed app up and running only few steps and about 10 minutes are needed. We will provsion the database service, create a table, load some data, then push the app to the IBM Cloud.

## Provision the SQL Database
1. Start by selecting the **Db2 Warehouse on Cloud** service in the **Data & Analytics** section of the catalog.
2.  Pick the Entry plan. Change the suggested service name to "sqldatabase" (we will use that name later on). Pick a region (data center) for the deployment of the database and make sure that the correct organization and space are selected.
3.  Click on **Create**. After a short moment you should get a success notification. You can click it away or wait until you are taken to the dashboard.

## Get Started with Db2 Warehouse on Cloud and create a table
We create the SQL database service in the form of Db2 Warehouse on Cloud. 

1. In the IBM Cloud dashboard locate the entry for the Db2 Warehouse on Cloud service. Click on it and you will be taken to the service dashboard. From here you can get to the documentation ("IBM Knowledge Center") under "Learn" or to the console (Web UI) for Db2 Warehouse on Cloud. Click on **Open**. The console is now loaded.
2. If it is the first time using the console, you are offered to take a tour. Take it. Remember how you can easily take the tour again. It is explained during the tour.
3. Click **Explore** in the navigation bar. It takes you to a list of existing schemas in the database. Locate the schema beginning with "DASH". Click on it.
4. Now we are creating the new table. Use the **"+ New Table"** for it. It brings up a form for the table name and its columns. Put in "cities" as table name. Copy the column definitions from the file [cityschema.txt](cityschema.txt) and paste them into box for the columns and data types.
5. Click on **Create** to define the new table.

## Load data
Now that the table "cities" has been created, we are going to load data into it.

1. Download and extract the file [cities1000.zip](http://download.geonames.org/export/dump/cities1000.zip) from [GeoNames](http://www.geonames.org/). It holds information about cities with a population of more than 1000. We are going to use it as data set.
2. In the top navigation of the Db2 console click on **Load**. This brings up the load dialog where you have a choice of loading data from your local machine, from cloud object storage (COS) with Swift interface (IBM Cloud / Softlayer) or from Amazon S3. You can also utilize the [Lift](https://console.bluemix.net/catalog/services/lift) migration service to transfer data from existing data sources. And if that's not enough you could [send in disk drives](https://www.ibm.com/support/knowledgecenter/SS6NHC/com.ibm.swg.im.dashdb.doc/learn_how/load_mail_in_drive.html) to quickly upload large amounts of data. For our case, uploading from the local machine will do.
3. In the "File selection" either use "browse files" to locate and pick the file "cities1000.txt" (see above) or drag it into that landing area. Click **Next** to get to the schema overview. Choose the schema starting with "DASH" again, then the table "CITIES". Because the table is empty it does not make a difference to either append to or overwrite existing data. Click on **Next** again.
4. The dialog shown then is used to customize how the data from the file "cities1000.txt" is interpreted during the load process. First, disable "Header in first row" because the file contains data only. Next, type in "0x09" as separator. It means that values within the file are delimited by tab(ulator). Last, pick "YYYY-MM-DD" as date format.
5. Click **Next** and you are offered to review the load settings. If you agree, click **Begin Load** to start loading the data into the "CITIES" table. The progress is displayed. Once the data is uploaded it should only take few seconds until the load is finished and some statistics are presented.

## Deploy the application code
The ready-to-run code for the database app is located in this Github repository. Clone or download the repository, then push it to the IBM Cloud. You need to be logged in to the region, org and space to which the database has been provisioned.

```
   cf push your-app-name
```

The file [manifest.yml](manifest.yml) tells the IBM Cloud to bind the app and the database service named "sqldatabase" together. No further configuration is needed. Once the push process is finished you should be able to access the app. Enjoy.

# Test and Expand the App
The app to display city information based on the loaded data set is reduced to a minimum. It offers a search form to specify a city name and few preconfigured cities. They are translated to either `/search?name=cityname` (search form) or `/city/cityname` (directly specified cities). Both requests are served from the same lines of code in the background. The cityname is passed as value to a prepared SQL statement using a parameter marker for security reasons. The rows are fetched from the database and passed to an HTML template for rendering.

Want to extend this app? Here are some ideas:
1. Offer a wildcard search on the alternate names.
2. Search for cities of a specific country and within a certain population values only.
3. Change the page layout by replacing the CSS styles and extending the templates.
4. Allow form-based creation of new city information or allow updates to existing data, e.g. population.

# Related Content
* Documentation: [IBM Knowledge Center for Db2 Warehouse on Cloud](https://www.ibm.com/support/knowledgecenter/en/SS6NHC/com.ibm.swg.im.dashdb.kc.doc/welcome.html)
* [Frequently asked questions about IBM Db2 on Cloud and IBM Db2 Warehouse on Cloud](https://www.ibm.com/support/knowledgecenter/SS6NHC/com.ibm.swg.im.dashdb.doc/managed_service.html) answering questions related to managed service, data backup, data encryption and security, and much more.
* [Free Db2 Developer Community Edition](https://www.ibm.com/us-en/marketplace/ibm-db2-direct-and-developer-editions) for developers
* Documentation: [API Description of ibm_db Python driver](https://github.com/ibmdb/python-ibmdb/wiki/APIs)
* [IBM Data Server Manager](https://www.ibm.com/us-en/marketplace/data-server-manager)
