# Register Task

> `airmail ecs register-task`

Registers a new task definition with ECS. The `family` property is defined automatically by Airmail and requires `org` and `name` be defined in the `config.yml` file.

## Task Environment Variables

The command will pull environment variables for the task from a file with the following naming structure: `<env>.env`. If you're deploying into an environment called `staging`, Airmail will look for a file called `staging.env` in the `.deploy` directory and use the variable declarations in the task.

Airmail uses the [`python-dotenv`](https://github.com/theskumar/python-dotenv) package to load the env files. Because of this you can also interpolate environment variables in the file [using POSIX variable expansion](https://github.com/theskumar/python-dotenv#usages). This is very handy when environment variables need to be secret.
