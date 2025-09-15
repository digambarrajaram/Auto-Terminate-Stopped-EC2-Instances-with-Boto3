"""
AWS Lambda function to automatically terminate 
stopped EC2 instances using Boto3.
"""

import boto3


def lambda_handler(_event, _context):
    """
    Entry point for the Lambda function.

    Args:
        _event (dict): AWS Lambda event payload (unused).
        _context (LambdaContext): AWS Lambda context object (unused).

    Returns:
        dict: HTTP-style response indicating termination status.
    """
    ec2 = boto3.client('ec2')

    response = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]
    )

    stopped_instances = [
        instance['InstanceId']
        for reservation in response['Reservations']
        for instance in reservation['Instances']
    ]

    if stopped_instances:
        print(f"Terminating stopped instances: {stopped_instances}")
        ec2.terminate_instances(InstanceIds=stopped_instances)
        return {
            'statusCode': 200,
            'body': f"Terminated instances: {stopped_instances}"
        }

    print("No stopped instances found.")
    return {
        'statusCode': 200,
        'body': "No stopped instances found."
    }
