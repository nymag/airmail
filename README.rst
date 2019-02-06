==============
Leviosa (WIP)
==============

    A CLI tool for deploying projects to AWS

Introduction/Philosophy
-----------------------

The point of Leviosa is to make deploying projects into AWS a little
easier. It was inspired as a binding layer between `Terraformed`_
infrastructure and deploying applications to `AWS ECS`_. At NYMag we
wanted to manage infrastructure with Terraform and then allow
applications to be more declarative about how they run without caring
about the infrastructure. A developer should be able to change easily
declare where and how their application will run and then be able to
easily configure resources in Terraform to support that. Leviosa is
designed to deploy code *with the assumption that the underlying
infrastructure is there to support the project*.

Naming
~~~~~~

We built an open-source CMS at NYMag called `Clay`_ that is comprised of
packages named after pottery/clay. Because this tool is meant to work
for any application going into ECS we didn't want to name it around
Clay, but...

``Clay --> Potter --> Harry Potter``

✨ `Wingardium Leviosa`_ ✨

It lifts project into the ☁️

How To
------

Leviosa needs to be run in a project with a ``.deploy`` directory. It
will look inside this directory for configuration files that will tell
the tool how to deploy to ECS.

::

   .
   ├── ...
   ├── .deploy                 # The directory holding the config
   │   ├── config.yml          # Holds the primary config declarations
   │   └── <env>.env           # Environment variable configuration for the container
   └── ...

Config File
~~~~~~~~~~~

`Config file docs coming soon`_

Local Development
-----------------

Currently configured to use ``watchcode`` for re-building:
`https://github.com/bluenote10/watchcode`_

.. _Terraformed: https://www.terraform.io/
.. _AWS ECS: https://docs.aws.amazon.com/ecs/index.html
.. _Clay: https://clay.nymag.com/
.. _Wingardium Leviosa: https://www.pottermore.com/book-extract-long/wingardium-leviosa
.. _Config file docs coming soon: ./docs/config.md
.. _`https://github.com/bluenote10/watchcode`: https://github.com/bluenote10/watchcode
