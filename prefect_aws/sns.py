"""SNS Block Module"""
import boto3
from prefect.blocks.core import Block
from pydantic import Field

from prefect_aws import AwsCredentials


class SNS(Block):
    """
    A block that facilitates interaction with AWS SNS.

    Attributes:
        value (str): The value to store.

    Example:
        Load a stored value:
        ```python
        from prefect_aws.sns import SNS
        block = SNS.load("BLOCK_NAME")
        block.publish("my subject", "my message")
        ```
    """

    _block_type_name = "SNS"
    _logo_url = "https://raw.githubusercontent.com/danielhstahl/prefect-sns/main/docs/img/aws-sns-simple-notification-service.svg"  # noqa
    _documentation_url = (
        "https://prefecthq.github.io/prefect-aws/sns/#prefect_aws.sns.SNS"  # noqa
    )

    sns_arn: str
    credentials: AwsCredentials = Field(
        default_factory=AwsCredentials,
        description="A block containing your credentials to AWS.",
    )

    def _get_sns_client(self) -> boto3.client:
        """
        Get SNS client from credentials
        """
        return self.credentials.get_boto3_session().client(
            "sns", region_name=self.credentials.region_name
        )

    def publish(self, subject: str, message: str):
        """
        Publishes message to SNS topic
        Example:
            Publish topic to sns
            ```python
            from prefect_aws.sns import SNS
            block = SNS.load("BLOCK_NAME")
            block.publish("my subject", "my message")
            ```
        """
        self._get_sns_client().publish(
            TopicArn=self.sns_arn,
            Message=message,
            Subject=subject,
        )