import boto3
import logging
import datetime
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# S3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Lambda function to archive S3 objects older than 6 months to Glacier storage class
    """
    # Set the bucket name - you can also pass this via environment variables
    bucket_name = 'aakash-serverless-architecture'
    
    # Calculate the date 6 months ago
    today = datetime.datetime.now()
    six_months_ago = today - datetime.timedelta(days=180)
    
    logger.info(f"Starting archival process for bucket: {bucket_name}")
    logger.info(f"Archiving files older than: {six_months_ago.strftime('%Y-%m-%d')}")
    
    try:
        # Get list of objects in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        
        # If no objects are found
        if 'Contents' not in response:
            logger.info(f"No objects found in bucket {bucket_name}")
            return {
                'statusCode': 200,
                'body': 'No objects found in bucket'
            }
        
        # Count statistics
        total_objects = 0
        archived_objects = 0
        
        # Process each object in the bucket
        for obj in response['Contents']:
            total_objects += 1
            key = obj['Key']
            last_modified = obj['LastModified']
            
            # Convert to datetime object for comparison
            last_modified_date = last_modified.replace(tzinfo=None)
            
            # Check if the object is older than 6 months
            if last_modified_date < six_months_ago:
                logger.info(f"Archiving object: {key}, Last Modified: {last_modified_date}")
                
                # Copy the object with new storage class
                s3_client.copy_object(
                    Bucket=bucket_name,
                    CopySource={'Bucket': bucket_name, 'Key': key},
                    Key=key,
                    StorageClass='GLACIER',
                    MetadataDirective='COPY'
                )
                
                archived_objects += 1
                logger.info(f"Successfully archived {key} to Glacier")
        
        # Process additional pages if the response was truncated
        while response.get('IsTruncated', False):
            continuation_token = response.get('NextContinuationToken')
            response = s3_client.list_objects_v2(
                Bucket=bucket_name,
                ContinuationToken=continuation_token
            )
            
            for obj in response.get('Contents', []):
                total_objects += 1
                key = obj['Key']
                last_modified = obj['LastModified']
                
                # Convert to datetime object for comparison
                last_modified_date = last_modified.replace(tzinfo=None)
                
                # Check if the object is older than 6 months
                if last_modified_date < six_months_ago:
                    logger.info(f"Archiving object: {key}, Last Modified: {last_modified_date}")
                    
                    # Copy the object with new storage class
                    s3_client.copy_object(
                        Bucket=bucket_name,
                        CopySource={'Bucket': bucket_name, 'Key': key},
                        Key=key,
                        StorageClass='GLACIER',
                        MetadataDirective='COPY'
                    )
                    
                    archived_objects += 1
                    logger.info(f"Successfully archived {key} to Glacier")
        
        logger.info(f"Archival process completed. Total objects: {total_objects}, Archived: {archived_objects}")
        
        return {
            'statusCode': 200,
            'body': f"Archival process completed. Total objects: {total_objects}, Archived: {archived_objects}"
        }
    
    except ClientError as e:
        logger.error(f"Error in archival process: {e}")
        return {
            'statusCode': 500,
            'body': f"Error in archival process: {str(e)}"
        }