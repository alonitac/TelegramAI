import time
import boto3
import json
from loguru import logger


def calc_backlog_per_instance():
    workers_queue = sqs.get_queue_by_name(QueueName=bot_to_worker_queue_name)
    msgs_in_queue = int(workers_queue.attributes.get('ApproximateNumberOfMessages'))
    asg_groups = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[autoscaling_group_name])['AutoScalingGroups']

    if not asg_groups:
        raise RuntimeError('Autoscaling group not found')
    else:
        asg_size = asg_groups[0]['DesiredCapacity']

    if msgs_in_queue == 0:
        backlog_per_instance = 0
    elif asg_size == 0:
        backlog_per_instance = 99
    else:
        backlog_per_instance = msgs_in_queue / asg_size

    return backlog_per_instance


def main():
    while True:
        backlog_per_instance = calc_backlog_per_instance()
        logger.info(f'backlog per instance: {backlog_per_instance}')

        # TODO send the backlog_per_instance metric to cloudwatch

        time.sleep(60)


if __name__ == '__main__':
    with open('../config.json') as f:
        config = json.load(f)

    bot_to_worker_queue_name = config.get('bot_to_worker_queue_name')
    autoscaling_group_name = config.get('autoscaling_group_name')

    sqs = boto3.resource('sqs', region_name=config.get('aws_region'))
    asg_client = boto3.client('autoscaling', region_name=config.get('aws_region'))

    main()
