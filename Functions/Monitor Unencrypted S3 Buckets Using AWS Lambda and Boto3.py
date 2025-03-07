import boto3
import json
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    """
    AWS Lambda function to detect S3 buckets without server-side encryption enabled.
    
    Args:
        event (dict): AWS Lambda event object
        context (object): AWS Lambda context object
        
    Returns:
        dict: Response containing list of unencrypted buckets
    """
    # Initialize the S3 client
    s3_client = boto3.client('s3')
    
    # Get list of all buckets
    try:
        buckets = s3_client.list_buckets()
    except ClientError as e:
        print(f"Error listing buckets: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error listing buckets: {str(e)}")
        }
    
    # List to store unencrypted buckets
    unencrypted_buckets = []
    
    # Check each bucket for encryption
    for bucket in buckets['Buckets']:
        bucket_name = bucket['Name']
        
        try:
            # Try to get the encryption configuration
            encryption = s3_client.get_bucket_encryption(Bucket=bucket_name)
            print(f"Bucket {bucket_name} has encryption enabled: {encryption}")
        except ClientError as e:
            # If we get NoSuchEncryptionConfiguration error, the bucket is not encrypted
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                unencrypted_buckets.append(bucket_name)
                print(f"Bucket {bucket_name} does not have server-side encryption enabled")
            else:
                print(f"Error checking encryption for bucket {bucket_name}: {e}")
    
    # Print summary
    if unencrypted_buckets:
        print(f"Found {len(unencrypted_buckets)} unencrypted buckets: {', '.join(unencrypted_buckets)}")
    else:
        print("All buckets have encryption enabled. Great job!")
    
    # Return the results
    return {
        'statusCode': 200,
        'body': json.dumps({
            'unencrypted_buckets': unencrypted_buckets,
            'count': len(unencrypted_buckets)
        })
    }