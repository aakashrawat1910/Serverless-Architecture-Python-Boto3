# Serverless-Architecture-Python-Boto3

This folder contains various AWS Lambda functions and their corresponding documentation for managing AWS resources using Boto3.

## Folder Structure

```
Documentation/
    Archive Old Files from S3 to Glacier Using AWS Lambda and Boto3.pdf
    Automated Instance Management Using AWS Lambda and Boto3.pdf
    Monitor Unencrypted S3 Buckets Using AWS Lambda and Boto3.pdf
    Restore EC2 Instance from Snapshot.pdf
Functions/
    Archive Old Files from S3 to Glacier Using AWS Lambda and Boto3.py
    Automated Instance Management Using AWS Lambda and Boto3.py
    Monitor Unencrypted S3 Buckets Using AWS Lambda and Boto3.py
    Restore EC2 Instance from Snapshot.py
```

## Documentation

- [Archive Old Files from S3 to Glacier Using AWS Lambda and Boto3](Documentation/Archive%20Old%20Files%20from%20S3%20to%20Glacier%20Using%20AWS%20Lambda%20and%20Boto3.pdf)
- [Automated Instance Management Using AWS Lambda and Boto3](Documentation/Automated%20Instance%20Management%20Using%20AWS%20Lambda%20and%20Boto3.pdf)
- [Monitor Unencrypted S3 Buckets Using AWS Lambda and Boto3](Documentation/Monitor%20Unencrypted%20S3%20Buckets%20Using%20AWS%20Lambda%20and%20Boto3.pdf)
- [Restore EC2 Instance from Snapshot](Documentation/Restore%20EC2%20Instance%20from%20Snapshot.pdf)

## Functions

### Archive Old Files from S3 to Glacier Using AWS Lambda and Boto3

This function archives S3 objects older than 6 months to the Glacier storage class.

```python
import boto3
import datetime

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = 'aakash-serverless-architecture'
    six_months_ago = datetime.datetime.now() - datetime.timedelta(days=180)
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    # ...
```

### Automated Instance Management Using AWS Lambda and Boto3

This function manages EC2 instances based on tags: stops instances tagged with `Action=Auto-Stop` and starts instances tagged with `Action=Auto-Start`.

```python
import boto3

ec2_client = boto3.client('ec2')

def lambda_handler(event, context):
    instances_to_stop = get_instances_by_tag(ec2_client, 'Action', 'Auto-Stop')
    instances_to_start = get_instances_by_tag(ec2_client, 'Action', 'Auto-Start')
    # ...
```

### Monitor Unencrypted S3 Buckets Using AWS Lambda and Boto3

This function detects S3 buckets without server-side encryption enabled.

```python
import boto3

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    buckets = s3_client.list_buckets()
    # ...
```

### Restore EC2 Instance from Snapshot

This function restores an EC2 instance from the latest snapshot of a given instance.

```python
import boto3
import datetime

ec2_client = boto3.client('ec2')

def lambda_handler(event, context):
    source_instance_id = 'i-0fedf73d9dabef09e'
    # ...
```

## Workflows

1. **Archive Old Files from S3 to Glacier**: This function runs periodically to move old files from S3 to Glacier.
2. **Automated Instance Management**: This function is triggered based on specific tags to start or stop EC2 instances.
3. **Monitor Unencrypted S3 Buckets**: This function runs periodically to check for unencrypted S3 buckets and logs the results.
4. **Restore EC2 Instance from Snapshot**: This function is triggered manually or by an event to restore an EC2 instance from the latest snapshot.

For more details, refer to the documentation PDFs in the `Documentation` folder.
