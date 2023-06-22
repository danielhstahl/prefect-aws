from moto import mock_sns
from moto.sns import sns_backends

from prefect_aws.sns import SNS


# @mock_sns
def test_sns_publishes(aws_credentials):
    with mock_sns():
        mock_topic = (
            aws_credentials.get_boto3_session()
            .client("sns", region_name="us-east-1")
            .create_topic(Name="mock-topic")
        )
        topic_arn = mock_topic.get("TopicArn")
        task = SNS(aws_credentials=aws_credentials, sns_arn=topic_arn)
        task.publish("mysubject", "mymessage")
        sns_backend = sns_backends["123456789012"]["us-east-1"]
        all_send_notifications = sns_backend.topics[topic_arn].sent_notifications
        assert all_send_notifications[0][1] == "mymessage"
        assert all_send_notifications[0][2] == "mysubject"
