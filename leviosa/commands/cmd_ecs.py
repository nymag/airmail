import click
import boto3
from leviosa.cli import pass_context
from leviosa.services.ecs_service import ECSService

# The ECS Service instance
ecs_service = ECSService()

@click.group(short_help='Create/modify ECS services')
@pass_context
def cli(ctx):
    ctx.add_line_break()
    ctx.preamble_log('Current Env', ecs_service.get_env())
    ctx.preamble_log('Project Name', ecs_service.get_name())
    ctx.preamble_log('Service Name', ecs_service.get_top_level_prop('service'))
    ctx.preamble_log('Project Cluster', ecs_service.get_top_level_prop('cluster'))
    ctx.preamble_log('Project Family', ecs_service.get_top_level_prop('family'))
    ctx.add_line_break()

@cli.command(name = 'deploy-service', short_help='Creates or updates a service based off the deploy configuration file')
@pass_context
def update_service(ctx):
    ctx.info_log('Running update-service...')
    ctx.info_log('This command will create an ECS service or update an existing service.')

    service_exists = ecs_service.service_exists() # Does the service exist?

    if service_exists:
        ecs_service.update_service()
    else:
        ecs_service.create_service()

@cli.command(name = 'register-task', short_help='Creates a task definition based off the deploy configuration file')
@pass_context
def updateTask(ctx):
    ctx.info_log('Running update-task...')
    ctx.info_log('This command will create a task definition for project based off the deploy configuration file')
    ctx.add_line_break()
    task_definition = ecs_service.create_task_definition()
    ecs_service.register_task_definition(task_definition)


@cli.command(name = 'build-image', short_help='Builds a Docker image and pushes to ECR based on your deploy configuration')
@pass_context
def buildImage(ctx):
    ctx.info_log('Running build-image...')
    ctx.info_log('This command will build the image for ')
    ctx.add_line_break()

    built_tag = ecs_service.build_container_image()
    ctx.info_log('Built project image: ' + built_tag)
