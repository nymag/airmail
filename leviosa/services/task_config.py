from functools import reduce
from nymdeploy.utils.files import read_yml,determine_project_path
from nymdeploy.utils.config import buildConfig
from pydash import set_

class TaskConfig():
    def __init__(self, getProp, getTopLevelProp, getWithPrefix):
        # Getters passed in to read from the config file
        # TODO: cleanup later? Pass in a different away
        self.getProp = getProp
        self.getTopLevelProp = getTopLevelProp
        self.getWithPrefix = getWithPrefix

        # The list of functions to reduce through
        self.transforms = [
            self.assignTaskInfo,
            self.assignTaskRoles,
            self.assignLogging,
            self.assignEnvVars
        ]

    def build(self):
        # The config that will be sent to AWS client
        config = read_yml(determine_project_path() + '/../data/task.yml')
        # Run throught the config builder reduce
        return buildConfig(self.transforms, config)

    def assignTaskRoles(self, config):
        account_id = self.getTopLevelProp('accountID')
        config['taskRoleArn'] = 'arn:aws:iam::' + account_id + ':role/' + self.getProp('taskRole')
        config['executionRoleArn'] = 'arn:aws:iam::' + account_id + ':role/' + self.getProp('executionRole')
        return config

    def setIntoContainerDefinition(self, config, prop, value):
        path = 'containerDefinitions[0].' + prop
        return set_(config, path, value)

    # Adds the desired count to the config
    def assignTaskInfo(self, config):
        config['family'] = self.getTopLevelProp('family')

        self.setIntoContainerDefinition(config, 'name', self.getTopLevelProp('name'))
        self.setIntoContainerDefinition(config, 'image', self.getTopLevelProp('family'))
        self.setIntoContainerDefinition(config, 'command', self.getProp('deployment.command'))
        self.setIntoContainerDefinition(config, 'cpu', self.getProp('deployment.cpu'))
        self.setIntoContainerDefinition(config, 'memory', self.getProp('deployment.memory'))
        self.setIntoContainerDefinition(config, 'portMappings[0].containerPort', self.getProp('deployment.port'))
        return config

    def assignLogging(self, config):
        self.setIntoContainerDefinition(config, 'logConfiguration.logDriver', self.getProp('logging.logDriver'))
        self.setIntoContainerDefinition(config, 'logConfiguration.options', self.getProp('logging.options'))
        return config

    def assignEnvVars(self, config):
        env_vars = []
        # TODO: make pathing more robust and with envs
        with open('./.deploy/qa.env') as f:
            for line in f.readlines():
                name, value = line.strip().split('=')
                env_vars.append({
                    'name': name,
                    'value': value
                })
        self.setIntoContainerDefinition(config, 'environment', env_vars)
        return config
