import boto3
import time
import urllib.request
import json

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

    # Call the plotting lambda via API Gateway
    api_url = 'https://ee3tkmt7h2.execute-api.us-east-1.amazonaws.com/stage11/plotFuntion'
    try:
        with urllib.request.urlopen(api_url) as response:  # Make a GET request to the API
            status_code = response.getcode()
            if status_code == 200:
                print("API call successful!")
            else:
                print(f"API call failed with status code: {status_code}")
    except Exception as e:
        print(f"Failed to call API: {str(e)}")

    return {
        'statusCode': 200,
        'body': 'Driver Lambda executed successfully!'
    }