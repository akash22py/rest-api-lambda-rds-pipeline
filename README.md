# rest-api-lambda-rds-pipeline
This repo contains data pipeline to perform CRUD operations using AWS API Gateway, Lambda function to process data using SQLAlchemy ORM and database created in RDS 
# API Gateway
Create a REST API on API gateway with individual resources and methods for CRUD operations and integrate it with lambda function using lambda proxy integration and deploy it.
# Lambda function
Create a lambda function to process the API requests and data from the RDS database created.
Also create layers for SQLAlchemy, typing_extensions and psycopg.
P.S. I have created a single zip file(python.zip) in lambda_layer folder for the above libraries, just upload that file in the lambda layer.
# RDS
Use RDS instance to create a database and connect it to DBeaver to create tables and view data in the backend.
