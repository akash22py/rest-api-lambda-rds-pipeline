import os
import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create the SQLAlchemy engine
engine = create_engine('postgresql://username:password@hostname:port/database_name')

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a base class for your models
Base = declarative_base()

# Define your model class
class MyModel(Base):
    # define your table name and columns 
    __tablename__ = 'eltp'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    salary = Column(Integer)

def create(event):
    data = json.loads(event['body'])

    # Create a session
    session = Session()

    try:
        # Create a new instance of MyModel
        new_instance = MyModel(id = data['id'],name=data['name'],salary=data['salary'])

        # Add the new instance to the session
        session.add(new_instance)

        # Commit the changes
        session.commit()

        return {
            'statusCode': 200,
            'body': 'Successfully created'
        }
    except Exception as e:
        # Handle any exceptions
        session.rollback()
        return {
            'statusCode': 500,
            'body': 'Error creating instance: ' + str(e)
        }
    finally:
        # Close the session
        session.close()

def read(event):
    session = Session()

    try:
        # Retrieve all instances of MyModel
        instances = session.query(MyModel).all()

        # Convert instances to a list of dictionaries
        result = [{'id': instance.id, 'name': instance.name,'salary': instance.salary} for instance in instances]

        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        # Handle any exceptions
        return {
            'statusCode': 500,
            'body': 'Error retrieving instances: ' + str(e)
        }
    finally:
        session.close()

def update(event):
    data = json.loads(event['body'])

    session = Session()

    try:
        # Retrieve the instance to update
        instance = session.query(MyModel).get(data['id'])

        if instance:
            # Update the instance with the new values
            instance.name = data['name']
            instance.salary = data['salary']

            # Commit the changes
            session.commit()

            return {
                'statusCode': 200,
                'body': 'Successfully updated'
            }
        else:
            return {
                'statusCode': 404,
                'body': 'Instance not found'
            }
    except Exception as e:
        # Handle any exceptions
        session.rollback()
        return {
            'statusCode': 500,
            'body': 'Error updating instance: ' + str(e)
        }
    finally:
        session.close()

def delete(event):
    data = json.loads(event['body'])

    session = Session()

    try:
        # Retrieve the instance to delete
        instance = session.query(MyModel).get(data['id'])

        if instance:
            # Delete the instance
            session.delete(instance)

            # Commit the changes
            session.commit()

            return {
                'statusCode': 200,
                'body': 'Successfully deleted'
            }
        else:
            return {
                'statusCode': 404,
                'body': 'Instance not found'
            }
    except Exception as e:
        # Handle any exceptions
        session.rollback()
        return {
            'statusCode': 500,
            'body': 'Error deleting instance: ' + str(e)
        }
    finally:
        session.close()

def lambda_handler(event, context):
    http_method = event['httpMethod']
    
    if http_method == 'GET':
        # Call the function to handle the GET method
        response = read(event)
    elif http_method == 'POST':
        # Call the function to handle the POST method
        response = create(event)
    elif http_method == 'PUT':
        # Call the function to handle the PUT method
        response = update(event)
    elif http_method == 'DELETE':
        # Call the function to handle the DELETE method
        response = delete(event)
    else:
        response = {
            'statusCode': 405,
            'body': 'Method not allowed'
        }
    
    return response
