from functools import reduce
from nymdeploy.utils.files import read_yml,determine_project_path
from nymdeploy.utils.config import buildConfig


class ServiceConfig():
    def __init__(self, getProp, getTopLevelProp, getWithPrefix):
        # Getters passed in to read from the config file
        # TODO: cleanup later? Pass in a different away?
        self.getProp = getProp
        self.getTopLevelProp = getTopLevelProp
        self.getWithPrefix = getWithPrefix

        # The list of functions to reduce through
        self.transforms = [
            self.assignLoadBalancer,
            self.assignServiceInfo,
            self.assignDeploymentConfiguration
        ]

    #
    def build(self, file):
        # The config that will be sent to AWS client
        config = read_yml(determine_project_path() + '/../data/' + file + '.yml')
        # Run throught the config builder reduce
        return buildConfig(self.transforms, config)

    # Adds the desired count to the config
    def assignServiceInfo(self, config):
        # UpdateService uses `service` and CreateService uses `serviceName`
        service_prop = 'service' if 'service' in config else 'serviceName'

        config['cluster'] = self.getTopLevelProp('cluster')
        config['taskDefinition'] = self.getTopLevelProp('family')
        config['desiredCount'] = self.getProp('deployment.desiredCount')
        config[service_prop] = self.getTopLevelProp('service')
        return config

    def assignDeploymentConfiguration(self, config):
        config['deploymentConfiguration']['maximumPercent'] = self.getProp('deployment.maxHealthyPercent', 200)
        config['deploymentConfiguration']['minimumHealthyPercent'] = self.getProp('deployment.minHealthyPercent', 80)
        return config

    # Adds load balancer information to the config
    def assignLoadBalancer(self, config):
        # Add if there is a `loadBalancers` prop in the dictionary
        if 'loadBalancers' in config:
            config['loadBalancers'][0]['targetGroupArn'] = self.getProp('loadBalancer.targetGroupArn')
            config['loadBalancers'][0]['containerName'] = self.getTopLevelProp('name')
            config['loadBalancers'][0]['containerPort'] = self.getProp('deployment.port')
        return config

    # TODO: Add some retriever/setter/validation functions
