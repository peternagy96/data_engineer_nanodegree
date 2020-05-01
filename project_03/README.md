# Project Summary

A music streaming startup, Sparkify, has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional tables. This will allow their analytics team to continue finding insights in what songs their users are listening to.

You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

In this project, you'll apply what you've learned on Spark and data lakes to build an ETL pipeline for a data lake hosted on S3. To complete the project, you will need to load data from S3, process the data into analytics tables using Spark, and load them back into S3. You'll deploy this Spark process on a cluster using AWS.

# How to run

Before startig, please create an S3 bucket named _dend-sparkify-datalake_. Create a _dwg.cfg_ file from the provided template and enter your IAM credinentials to be able to access this bucket.

In order to run the ETL process, run

```bash
python etl.py
```

# Files

- **etl<span></span>.py:** Contains the code that describes the ETL pipeline ingesting and transforming song and log data with Spark from an S3 bucket to another one.

# Dataset

The dataset is a subset of real data from the [Million Song Dataset](http://millionsongdataset.com/). The files are in a JSON format and contain metadata about songs and artists. The files are partitioned by the first three letters of each song's track ID.

# Database schema design

For efficient data analysis a Relational Database Schema is created, which is filled with data from the json files using the ETL pipeline.

A star schema is used, which allows the business stake holders to aggragate different parts of the data efficiently. This schema uses a single fact table _(songplays)_ containing song information. There are four different dimension tables relating to the fact table _(users, songs, artists, time)_, all of which allow to extract specific information needed to make business decisions.
