import boto3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from decimal import Decimal

import numpy as np

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
bucket_name = 'testbucket2270'
table = dynamodb.Table('S3-object-size-history')

def lambda_handler(event, context):
    # Query DynamoDB for last 10 seconds
    now = datetime.utcnow()
    ten_seconds_ago = now - timedelta(seconds=15)

    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('bucket_name').eq(bucket_name) &
                               boto3.dynamodb.conditions.Key('timestamp').between(ten_seconds_ago.isoformat(), now.isoformat())
    )

    # Extract data for plotting
    timestamps = [item['timestamp'] for item in response['Items']]
    sizes = [float(item['total_size']) for item in response['Items']]  # Convert Decimal to float

    # Convert timestamps to datetime objects
    timestamps = [datetime.fromisoformat(ts) for ts in timestamps]

    # Check if there are any data points
    if not timestamps or not sizes:
        return {
            'statusCode': 204,
            'body': 'No data found to plot.'
        }

    # Create the plot
    Max_values = np.ones_like(sizes) * 1.0 * max(sizes)  # Create an array of maximum values
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, Max_values, label='Maximum size')
    plt.plot(timestamps, sizes, label='Bucket Size over Time', marker='o')  # Add markers to see points
    plt.xlim([ten_seconds_ago, now])  # Set x-axis limits to the last 10 seconds
    plt.xlabel('Time')
    plt.ylabel('Size (Bytes)')
    plt.title('S3 Bucket Size Change')
    plt.legend()

    # Set y-axis limit based on sizes
    plt.ylim(bottom=0)  # Set a lower limit for the y-axis
    if sizes:  # Check if sizes list is not empty
        plt.ylim(top=max(sizes) * 1.1)  # Set upper limit a bit above the max size

    # Save plot locally and upload to S3
    plot_filename = '/tmp/plot.png'
    plt.savefig(plot_filename)
    plt.close()  # Close the plot to avoid display issues

    # Upload to S3
    s3.upload_file(plot_filename, bucket_name, 'plot.png')

    return {
        'statusCode': 200,
        'body': 'Plot created and uploaded!'
    }