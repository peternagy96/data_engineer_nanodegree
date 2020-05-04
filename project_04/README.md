# Project Summary

A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

They have decided to bring you into the project and expect you to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to

# How to run

Before startig, please create a Redshift cluster on AWS and provide your creditentials in the Airflow UI. Then enable the DAG in the Airflow UI.

# Files

- **load_data_to_redshift:** This file contains the description of the DAG, which loads the files from S3 to Redshift

- **sql_queries:** Helper class for the SQL INSERT statements.

- **operators:** The four files in the operators folder describe the four type of Airflow workflow steps that are needed to complete the DAG.

# Dataset

The dataset is a subset of real data from the [Million Song Dataset](http://millionsongdataset.com/). The files are in a JSON format and contain metadata about songs and artists. The files are partitioned by the first three letters of each song's track ID.

# Database schema design

For efficient data analysis a Relational Database Schema is created, which is filled with data from the json files using the ETL pipeline.

A star schema is used, which allows the business stake holders to aggragate different parts of the data efficiently. This schema uses a single fact table _(songplays)_ containing song information. There are four different dimension tables relating to the fact table _(users, songs, artists, time)_, all of which allow to extract specific information needed to make business decisions.
