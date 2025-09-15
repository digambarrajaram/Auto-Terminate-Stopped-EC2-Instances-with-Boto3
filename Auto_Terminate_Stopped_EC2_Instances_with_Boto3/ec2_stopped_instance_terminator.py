import boto3


"""
AWS Lambda function to automatically terminate stopped EC2 instances.
"""
def lambda_handler(event, context):
    """
    Entry point for the Lambda function.

    Args:
        event (dict): AWS Lambda event payload.
        context (LambdaContext): AWS Lambda context object.

    Returns:
        dict: HTTP-style response indicating termination status.
    """
    ec2 = boto3.client('ec2')

    # Get all stopped instances
    response = ec2.describe_instances(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['stopped']}
        ]
    )

    stopped_instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            stopped_instances.append(instance_id)

    # If any stopped instances found, terminate them
    if stopped_instances:
        print(f"Terminating stopped instances: {stopped_instances}")
        ec2.terminate_instances(InstanceIds=stopped_instances)
        return {
            'statusCode': 200,
            'body': f"Terminated instances: {stopped_instances}"
        }
    else:
        print("No stopped instances found.")
        return {
            'statusCode': 200,
            'body': "No stopped instances found."
        }
