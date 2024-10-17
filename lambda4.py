import boto3
import time

s3 = boto3.client('s3')
bucket_name = 'testbucket2270'

def lambda_handler(event, context):
    # Create object
    s3.put_object(Bucket=bucket_name, Key='assignment1.txt', Body='Empty Assignment 1')
    time.sleep(5)

    # Update object
    s3.put_object(Bucket=bucket_name, Key='assignment1.txt', Body='Empty Assignment 2222222222')
    time.sleep(5)

    # Delete object
    s3.delete_object(Bucket=bucket_name, Key='assignment1.txt')
    time.sleep(5)

    # Create another object
    s3.put_object(Bucket=bucket_name, Key='assignment2.txt', Body='33')
    time.sleep(5)

    # Call the plotting lambda
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='plotFunction')

    return {
        'statusCode': 200,
        'body': 'Driver Lambda executed successfully!'
    }
