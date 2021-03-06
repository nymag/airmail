import os, sys
import click
from .utils import read_yml
from pydash import get, set_
import boto3

class DeployFile():
    def __init__(self, env, config):
        # Grab cwd
        self.cwd = os.getcwd()
        # Grab file
        self.file_path = "{cwd}/.deploy/{config}".format(cwd=self.cwd, config=config)
        # Read file or throw
        self.deploy_json = read_yml(self.file_path)
        # The environment
        self.env = env

        # Build some properties here
        # TODO: make it a reduce? :)
        self.inject_cluster_and_family()
        self.inject_aws_account_id()
        self.build_image_id()

    # Add top level account id
    def inject_aws_account_id(self):
        id = boto3.client('sts').get_caller_identity().get('Account')
        set_(self.deploy_json, 'accountID', id)

    # Grab the name from the file
    def get_name(self):
        return self.get_top_level_prop('name')

    # Grab the org name
    def get_org(self):
        return self.get_top_level_prop('org')

    def get_service(self):
        """Get the service name from the config file"""
        prop = "{env}.service".format(env=self.env)
        env_service_declaration = get(self.deploy_json, prop, False)
        return env_service_declaration

    def build_image_id(self):
        image_tag = "{tag}.dkr.ecr.us-east-1.amazonaws.com/{name}".format(tag=self.get_top_level_prop('accountID'), name=self.get_with_prefix('name', '/'))
        set_(self.deploy_json, '.imageID', image_tag)

    def get_with_prefix(self, prop, delim='-'):
        """Retrieve a value with <ORG>-<ENV>- prefix. Can pass in custom delimiter """

        if prop not in self.deploy_json:
            return None

        top_level = self.get_top_level_prop(prop)
        value = top_level if top_level != None else self.get_prop(prop)
        return self.get_org() + delim + self.env + delim + value


    def inject_cluster_and_family(self):
        """Assign the cluster and family for the service/task using the `name` and `cluster` fields if set"""

        cluster_val = self.get_with_prefix('cluster')
        family_val = self.get_with_prefix('name')

        if cluster_val is None:
            cluster_val = self.get_with_prefix('name')

        set_(self.deploy_json, '.cluster', cluster_val)
        set_(self.deploy_json, '.family', family_val)

    #  Get a tol level property
    def get_top_level_prop(self, prop, default=None):
        """Retrieve a property's value from the top level of the config"""
        return get(self.deploy_json, prop, default)

    # Grab a property from the specific env
    def get_prop(self, prop, default=None):
        """Get a property's value that is nested in the env object"""
        prop = self.env + '.' + prop
        return get(self.deploy_json, prop, default)
