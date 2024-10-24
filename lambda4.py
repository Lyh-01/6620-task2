import boto3
import time

s3 = boto3.client('s3')
bucket_name = 'testbucket2270'

def lambda_handler(event, context):
    # Create object
    s3.put_object(Bucket=bucket_name, Key='assignment1.txt', Body='Empty Assignment 1')
    time.sleep(2)

    # Update object
    s3.put_object(Bucket=bucket_name, Key='assignment1.txt', Body='Empty Assignment 2222222222')
    time.sleep(2)

    # Delete object
    response = s3.delete_object(Bucket=bucket_name, Key='assignment1.txt')
    print(response)
    time.sleep(2)

    # Create another object
    s3.put_object(Bucket=bucket_name, Key='assignment2.txt', Body='33')
    time.sleep(2)

    # Call the plotting lambda
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='plotFunction')

    return {
        'statusCode': 200,
        'body': 'Driver Lambda executed successfully!'
    }