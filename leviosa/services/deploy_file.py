import os, sys
import click
from .utils import read_yml
from pydash import get, set_
import boto3

class DeployFile():
    def __init__(self, env):
        # Grab cwd
        self.cwd = os.getcwd()
        # Grab file
        self.file_path = self.cwd + '/.deploy/config.yml'
        # Read file or throw
        self.deploy_json = read_yml(self.file_path)
        # The environment
        self.env = env

        # Build some properties here
        # TODO: make it a reduce? :)
        self.buildClusterAndFamily()
        self.injectAWSAccountId()

    # Add top level account id
    def injectAWSAccountId(self):
        id = boto3.client('sts').get_caller_identity().get('Account')
        set_(self.deploy_json, 'accountID', id)

    # Grab the name from the file
    def getName(self):
        return self.getTopLevelProp('name')

    # Grab the org name
    def getOrg(self):
        return self.getTopLevelProp('org')

    # Get the value but prefix with `<ORG>-<ENV>-`
    def getWithPrefix(self, prop, delim='-'):
        topLevel = self.getTopLevelProp(prop)
        value = topLevel if topLevel != None else self.getProp(prop)

        return self.getOrg() + delim + self.env + delim + value


    def buildClusterAndFamily(self):
        """Using the `name`, assign the cluster and family for the service/task"""

        cluster_val = self.getWithPrefix('name')
        set_(self.deploy_json, '.cluster', cluster_val)
        set_(self.deploy_json, '.family', cluster_val)

    #  Get a tol level property
    def getTopLevelProp(self, prop, default=None):
        """Retrieve a property's value from the top level of the config"""

        return get(self.deploy_json, prop, default)

    # Grab a property from the specific env
    def getProp(self, prop, default=None):
        """Get a property's value that is nested in the env object"""
        prop = self.env + '.' + prop
        return get(self.deploy_json, prop, default)
