from moto import mock_sns

from prefect_aws.sns import SNS


@mock_sns
def test_sns_publishes(aws_credentials):
    task = SNS(aws_credentials=aws_credentials, sns_arn="some_test_arn")
    task.publish("mysubject", "mymessage")
    assert True
