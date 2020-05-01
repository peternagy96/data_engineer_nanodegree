# Project Summary

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

# How to run

Before startng, please create an AWS Redshiuft cluster with an IAM role to be able to access it. Create a _dwg.cfg_ file from the provided template and enter your credinentials.

In order to create the database with its tables, please run

```bash
python create_tables.py
```

The full ETL process can be run with

```bash
python etl.py
```

# Files

- **sql_queries.py:** Contains all necessary SQL queries to create and drop the necessary tables and insert data into them

- **create_tables.py:** Creates the DB tables in an AWS Redshift cluster

- **etl<span></span>.py:** Contains the code that describes the ETL pipeline ingesting song and log data from S3 buckets to a Redshift cluster

# Dataset

The dataset is a subset of real data from the [Million Song Dataset](http://millionsongdataset.com/). The files are in a JSON format and contain metadata about songs and artists. The files are partitioned by the first three letters of each song's track ID.

# Database schema design

For efficient data analysis a Relational Database Schema is created, which is filled with data from the json files using the ETL pipeline.

A star schema is used, which allows the business stake holders to aggragate different parts of the data efficiently. This schema uses a single fact table _(songplays)_ containing song information. There are four different dimension tables relating to the fact table _(users, songs, artists, time)_, all of which allow to extract specific information needed to make business decisions.
