# Config File

The `config.yml` file should live in a `.deploy` directory at the root of your project. Before proceeding it will help to read [the assumptions around infrastructure naming](https://github.com/nymag/airmail/blob/master/docs/infrastructure-assumptions.md) that this tool makes.

### Example Config File
```yaml
name: coolapp
org: myorg
projectDirectory: app

qa:
  service: coolservice
  taskRole: myCoolRole
  executionRole: myCoolTaskExecutionRole
  deployment:
    command: ["npm", "start"]
    cpu: 1
    memory: 128
    port: 3001
    desiredCount: 1
    version: latest # optional
    maxHealthyPercent: 150 # optional
    minHealthyPercent: 100 # optional
  loadBalancer:
    targetGroupArn: target::group::arn
  logging:
    logDriver: syslog
    options:
      syslog-address: udp://<ip_address>:2233
```

## Top Level Properties

Below are a list of all the top level properties required in the config file. There are three required top level properties and then environment specific configuration declarations.

#### Name

> `name` (string)

This should be the name of the application you're deploying. It's value will be used to compute the following:

  - The ECR repo to push the image to
  - The name of the container in the task definition
  - The name of the cluster to deploy into

#### Org

> `org` (string)

This property is used to namespace all ECR repos and clusters in your AWS setup. It's used in few places in [the assumptions](https://github.com/nymag/airmail/blob/master/docs/infrastructure-assumptions.md) document.

  - The top-level namespace of ECR repo's
  - The top-level namespace of all ECS clusters

#### Project Directory

> `projectDirectory` (string)

This is just the directory where your application can be found relative to the `.deploy` directory you're running the command from. The assumption here is that there will be a Dockerfile in the directory you point to and that the application will be in the same directory.


### Environment Specific Config

After the top level properties of `name`, `org`, and `projectDirectory` you will begin to define configuration for each environment. To do this simply define a new property that is the name of your environment. For this example we will proceed with an environment called `qa`, but this name can be anything that makes sense for your setup. The values of these properties have direct correlation to properties for ECS task/service declarations.

#### `<ENV>.service`

> (string)

The name of the ECS service deployed into the cluster.

#### `<ENV>.taskRole`

> string

The IAM role the container assumes when runnning. Find more details here: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html#task_role_arn

#### `<ENV>.executionRole`

> string

The IAM role for pulling from ECR/publishing container logs to Cloudwatch. Find more details here: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html#execution_role_arn

#### `<ENV>.deployment`

> object

An object with different properties related to the deployment of the ECS task. Values in here directly correspond to the container runtime environment. Details can be found here: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html#container_definition_environment

##### `<ENV>.deployment.command`

> array (optional)

The command to run inside the container to begin running.

##### `<ENV>.deployment.cpu`

> integer

The number of CPU units the ECS container agent will reserve for the container

##### `<ENV>.deployment.memory`

> integer

The amount of memory (in MiB) used by the task

##### `<ENV>.deployment.port`

> integer

The port the container exposes. Used for load balancing

##### `<ENV>.deployment.desiredCount`

> integer

The number of instances of the task to run


##### `<ENV>.deployment.version`

> string (optional)

The version to use for tagging the container image when building. If this value is not defined then it will be pulled from the `version` property in the `package.json` file in the same directory of the Dockerfile used for building the application

##### `<ENV>.deployment.maxHealthyPercent`

> integer (optional) [default: 200]

The upper limit on the number of tasks your service will run. More info: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/basic-service-params.html


##### `<ENV>.deployment.minHealthyPercent`

> integer (optional) [default: 80]

The lower limit on the number of tasks your service will run. More info: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/basic-service-params.html

#### `<ENV>.loadBalancer`

> object (optional)

Right now Airmail assumes you're load balancing your deployment. It's super rudimentary and will be worked on soon.

##### `<ENV>.loadBalancer.targetGroupArn`

> string (optional)

The ARN of the target group for an ALB

#### `<ENV>.logging`

> object (optional)

An object for configuring the log driver of your task definition. More details: https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_LogConfiguration.html

##### `<ENV>.logging.logDriver`

> string (optional)

The name of the log driver to use. See logging documentation provided by AWS for valid values.

##### `<ENV>.logging.options`

> object (optional)

An object of options passed to the logging driver. These options depend on the logging driver used.
