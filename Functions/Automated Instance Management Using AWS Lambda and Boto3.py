import boto3
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda function to manage EC2 instances based on tags:
    - Stops instances tagged with Action=Auto-Stop
    - Starts instances tagged with Action=Auto-Start
    """
    # Initialize boto3 EC2 client
    ec2_client = boto3.client('ec2')
    
    # Find instances to stop (Action=Auto-Stop)
    instances_to_stop = get_instances_by_tag(ec2_client, 'Action', 'Auto-Stop')
    
    # Find instances to start (Action=Auto-Start)
    instances_to_start = get_instances_by_tag(ec2_client, 'Action', 'Auto-Start')
    
    # Stop instances
    stop_result = stop_instances(ec2_client, instances_to_stop)
    
    # Start instances
    start_result = start_instances(ec2_client, instances_to_start)
    
    # Prepare and return the results
    return {
        'statusCode': 200,
        'body': {
            'StoppedInstances': stop_result,
            'StartedInstances': start_result
        }
    }

def get_instances_by_tag(ec2_client, tag_key, tag_value):
    """
    Find EC2 instances that have a specific tag key and value
    """
    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': f'tag:{tag_key}',
                'Values': [tag_value]
            },
            {
                'Name': 'instance-state-name',
                'Values': ['pending', 'running', 'stopping', 'stopped']
            }
        ]
    )
    
    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
            logger.info(f"Found instance {instance['InstanceId']} with tag {tag_key}={tag_value}")
    
    return instance_ids

def stop_instances(ec2_client, instance_ids):
    """
    Stop the specified EC2 instances if they are in 'running' state
    """
    if not instance_ids:
        logger.info("No instances to stop")
        return []
    
    # First, check which instances are running
    response = ec2_client.describe_instances(
        InstanceIds=instance_ids,
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )
    
    running_instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            running_instances.append(instance['InstanceId'])
    
    # Stop only running instances
    if running_instances:
        logger.info(f"Stopping instances: {running_instances}")
        ec2_client.stop_instances(InstanceIds=running_instances)
        return running_instances
    else:
        logger.info("No running instances to stop")
        return []

def start_instances(ec2_client, instance_ids):
    """
    Start the specified EC2 instances if they are in 'stopped' state
    """
    if not instance_ids:
        logger.info("No instances to start")
        return []
    
    # First, check which instances are stopped
    response = ec2_client.describe_instances(
        InstanceIds=instance_ids,
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['stopped']
            }
        ]
    )
    
    stopped_instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            stopped_instances.append(instance['InstanceId'])
    
    # Start only stopped instances
    if stopped_instances:
        logger.info(f"Starting instances: {stopped_instances}")
        ec2_client.start_instances(InstanceIds=stopped_instances)
        return stopped_instances
    else:
        logger.info("No stopped instances to start")
        return []