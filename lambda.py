import boto3

# Create the S3 bucket
s3 = boto3.client('s3')
bucket_name = 'testbucket2270'

def create_s3_bucket():
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"S3 bucket {bucket_name} created successfully!")
    except Exception as e:
        print(f"Error creating bucket: {e}")

# Create the DynamoDB table
dynamodb = boto3.client('dynamodb')
table_name = 'S3-object-size-history'

def create_dynamodb_table():
    try:
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'bucket_name', 'KeyType': 'HASH'},  # Partition key
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}   # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'bucket_name', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print(f"DynamoDB table {table_name} created successfully!")
    except Exception as e:
        print(f"Error creating DynamoDB table: {e}")

if __name__ == '__main__':
    create_s3_bucket()
    create_dynamodb_table()
