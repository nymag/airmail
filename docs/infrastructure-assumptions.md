# Infrastructure Assumptions

Airmail is built with certain assumptions around your infrasturcture naming
conventions. At NYMag we use Terraform to provision our infrastructure and the
naming is built to mirror that. We recognize that these conventions won't work
for everyone and are looking to make this more flexible as the tool continues
to develop. Below is a list of the naming conventions we expect by service. The
[`config.yml`](https://github.com/nymag/airmail/blob/master/docs/config.md)
will try to reference this documentation to explain why certain properties are
required.

> One big thing to highlight is that this tool currently assumes you're
> deploying an application to a cluster with only one container. In the future
> we'll support multi-container task definitions.


## ECS

- Cluster: the cluster naming convention we follow is
`<organization>-<env>-<application_name>`. We have a cluster for every
environment for each application and that cluster has every ECS needed to to
support that application. For our CMS (Clay), we run three clusters:
`nymag-qa-clay`, `nymag-stg-clay` and `nymag-prd-clay`.

- Service: the service name is unique to the application you're deploying so we
have no assumptions there

- Task: the name of the container in the task definition should just be the
name of the application. Makes it easy to refer to.


## ECR

- Repo: we name the repo in the followiing way:
`<organization>/<env>/<application_name>`. In this way we provision a repo for
each environment for each application. AWS recently added more robust support
of for tagging which we plan to leverage and may update this approach to
reflect that.
