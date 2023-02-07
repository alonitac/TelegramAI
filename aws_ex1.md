# AWS Ex1 - Provision the TelegramAI app in AWS

## Background

Your goal is to provision the TelegramAI chat app as a scalable, micro-services architecture in AWS.

Here is a high level diagram of the architecture:

![](img/botaws2.png)

## Scaling the app

When end-users send a message via Telegram app (1-black), the messages are served by the Bot service (run as a Docker container in the Telegram Bot EC2 instance).
The Bot service **doesn't** download the video from YouTube itself, otherwise, all it does is sending a "job" to an SQS queue (2-black), and return the end-user a message like "your video is being downloaded...".
So, the Bot service is a very lightweight app that can serve hundreds requests per seconds. 
In the other side, there are Worker service (run as a Docker container in the Worker EC2 instance) **consumes** jobs from the SQS queue (3-black) and does the hard work - to download the video from YouTube and upload it to S3 (4-black). When the Worker done with current job, it asks the SQS queue if it has another job for him. As long as there are jobs pending in the queue, a free Worker will consume and perform the job. In such way the Bot service pushes jobs to the SQS queue, making it "full", while the Worker service consumes jobs from the queue, making it "empty".

But what if the rate in which the Bot service is pushing jobs to the queue is much higher than the rate the Worker completing jobs? In such case the queue will overflow...
To solve that, we will create multiple workers that together consume jobs from the queue. How many workers? we will deploy a dynamic model **that auto-scale the number of workers** depending on the number of messages in the queue. 
When there are a lot of jobs in the queue, the autoscaler will provision many workers. 
When there are only a few jobs in the queue, the autoscaler will provision fewer workers.
The Workers are part of an AutoScaling group, which is scaled in and out by a custom metric that the Metric Sender service (run as a Docker container as well, on the same VM as the Bot service) writes to CloudWatch every 1 minute (1-blue). CloudWatch will trigger an autoscale event (2-blue) when needed, which results in provisioning of another Worker instance, or terminate a redundant Worker instance (3-blue). 

The metric sent to CloudWatch can be called `BacklogPerInstance`, as it represents the number of jobs in the queue (jobs that was not consumed yet) per Worker instance.
For example, assuming you have 5 workers up and running, and 100 messages in the queue, thus `BacklogPerInstance` equals 20, since each Worker instance has to consume ~20 messages to get the queue empty. For more information, read [here](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-using-sqs-queue.html).

### The TelegramAI repo structure 

The repository structure is divided into services - each service under its own directory, while all services are sharing common files (`config.json` and `utils.py`) under the root directory of the repo.

1. `bot/app.py` - The Telegram bot code, similar to what you've implemented in the previous exercise. But this time, the bot doesn't download the videos itself, but sends a "job" to an SQS queue.
2. `worker/app.py` - The Worker service continuously reads messages from the SQS queue and process them, which means download the video from YouTube and store it in a dedicated S3 bucket.
3. `metric-sender/app.py` - The Metric Sender service calculates the `backlog_per_instance` metric and send it to CloudWatch.

Each service has its own `Dockerfile` under the service's directory.
