import click
import boto3
from leviosa.cli import pass_context
from leviosa.services.ecs_service import ECSService

# The ECS Service instance
ecs_service = ECSService()

@click.group(short_help='Create/modify ECS services')
@pass_context
def cli(ctx):
    ctx.addLineBreak()
    ctx.preambleLog('Current Env', ecs_service.getEnv())
    ctx.preambleLog('Project Name', ecs_service.getName())
    ctx.preambleLog('Service Name', ecs_service.getTopLevelProp('service'))
    ctx.preambleLog('Project Cluster', ecs_service.getTopLevelProp('cluster'))
    ctx.preambleLog('Project Family', ecs_service.getTopLevelProp('family'))
    ctx.addLineBreak()

@cli.command(name = 'update-service', short_help='Creates or updates a service based off the deploy.yml file in the current directory')
@pass_context
def updateService(ctx):
    ctx.infoLog('Running update-service...')
    ctx.infoLog('This command will create an ECS service or update an existing service.')
    ctx.addLineBreak()
    # Does the service exist?
    service_exists = ecs_service.serviceExists()

    if service_exists:
        print('foo')
        ecs_service.updateService()
    else:
        print('bar')
        ecs_service.createService()

@cli.command(name = 'update-task', short_help='Creates a task definition based off the deploy.yml file in the current directory')
@pass_context
def updateTask(ctx):
    ctx.infoLog('Running update-task...')
    ctx.infoLog('This command will create a task definition for project based off the deploy.yml file in your current directory')
    ctx.addLineBreak()

    task_definition = ecs_service.createTaskDefinition()
    print(task_definition)
    ecs_service.registerTaskDefinition(task_definition)


@cli.command(name = 'build-image', short_help='Creates a task definition based off the deploy.yml file in the current directory')
@pass_context
def buildImage(ctx):
    ctx.infoLog('Running build-image...')
    ctx.infoLog('This command will build the image for ')
    ctx.addLineBreak()

    ecs_service.buildContainerImage()
