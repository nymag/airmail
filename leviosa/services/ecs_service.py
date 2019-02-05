from .deploy_file import DeployFile
import boto3
import click
from botocore.exceptions import ClientError
from .utils import errLog
from .service_config import ServiceConfig
from .task_config import TaskConfig
from nymdeploy.utils.bash import runScript
import subprocess

class ECSService(DeployFile):
    def __init__(self):
        # ECS client
        self.client = boto3.client('ecs')
        # The env
        self.env = 'qa'

        # Init the Deploy File class
        DeployFile.__init__(self, self.env)

        self.ServiceConfigBuilder = ServiceConfig(self.getProp, self.getTopLevelProp, self.getWithPrefix)
        self.TaskConfigBuilder = TaskConfig(self.getProp, self.getTopLevelProp, self.getWithPrefix)

    def getEnv(self):
        return self.env

    # Check if a service exists
    def serviceExists(self):
        """Given the config.yml file, check if the service exists in the target cluster"""

        cluster = self.getTopLevelProp('cluster')
        service_name = self.getTopLevelProp('service')

        try:
            # Make the request
            response = self.client.describe_services(
                cluster=cluster,
                services=[ service_name ]
            )

            # Grab the failures
            failures = response['failures']

            if len(failures) >= 1:
                return False
            else:
                return True

        except ClientError as e:
            if e.response['Error']['Code'] == 'ClusterNotFoundException':
                # If hitting this, the cluster does not exist
                errLog('Cluster not found!')
            else:
                click.echo('Unexpected error: ' + e)

    def createService(self):
        """Create a service using the config.yml and default config (data/service.yml)"""
        # Build the config object
        config = self.ServiceConfigBuilder.build('service')

        print('From create service')
        print(config)
        response = self.client.create_service(**config)
        print(response)

    def updateService(self):
        config = self.ServiceConfigBuilder.build('service_update')
        print('From update service')
        print(config)
        response = self.client.update_service(**config)
        print(response)

    def createTaskDefinition(self):
        """Return the JSON for a task definition"""
        return self.TaskConfigBuilder.build()

    def buildContainerImage(self):
        ecr_repo = self.getWithPrefix('name', '/')
        version = "latest" # TODO: Need to make dynamic
        image_tag = self.getTopLevelProp('accountID') + ".dkr.ecr.us-east-1.amazonaws.com/" + ecr_repo + ":" + version
        env_dict = {
            'VERSION': version,
            'ECR_REPO': ecr_repo,
            'TASK_IMAGE_TAG': image_tag
        }

        val = runScript('ecr_push', env_dict)

        if (val == 0):
            print('Build succeeded!')
        else:
            print('The image build went poorly')

    def registerTaskDefinition(self, task):
        """Given task definition JSON, make the container and create a task definition"""

        response = self.client.register_task_definition(**task)
        print(response)
