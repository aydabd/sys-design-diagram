=====================
System Design Diagram
=====================

A Docker container for generating system design diagrams using PlantUML and the diagrams library.

.. image:: https://img.shields.io/badge/Docker-Ready-blue.svg
    :target: https://www.docker.com/

.. image:: https://img.shields.io/badge/license-MIT-green.svg
    :target: https://opensource.org/licenses/MIT

.. image:: https://github.com/aydabd/sys-design-diagram/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/aydabd/sys-design-diagram/actions/workflows/ci.yml

.. contents::
    :local:
    :depth: 2

Overview
========

System Design Diagram is a Docker container that provides tools to generate system design diagrams from PlantUML files and using the diagrams library. This container is designed for use in CI/CD pipelines and other automation workflows.

Features
========

- Generate diagrams from PlantUML files
- Generate diagrams using the diagrams library
- Process all diagrams in a given directory
- Asynchronous processing for better performance

Installation
============

To use the Docker container, pull it from the GitHub Container Registry or docker hub:

.. code-block:: bash

    docker pull ghcr.io/aydabd/sys-design-diagram:latest
    docker pull aydabd/sys-design-diagram:latest

Make sure you have Docker installed and running on your system.

Usage
=====

The Docker container provides several commands to generate diagrams:

.. code-block:: bash

    docker run --rm --it ghcr.io/aydabd/sys-design-diagram:latest [OPTIONS] COMMAND [ARGS]...

Options
-------

- `-v`, `--verbose`: Enable verbose mode.
- `--version`: Show the version and exit.
- `--help`: Show the help message and exit.

Commands
--------

- `diagrams`: Generate diagrams using the diagrams library.
- `plantuml`: Generate diagrams from PlantUML files.
- `process-all`: Generate diagrams using both PlantUML and diagrams library.

Examples
========

There is a `compose.yaml`_ file which can be used to generate diagrams from a tests-data directory. To use the `compose.yaml` file, run the following command:

.. code-block:: bash

    docker-compose up --build

Development
===========

To contribute to the development of this project, follow these steps:

1. Clone the repository
2. for linux users, install mamba-githook [mamba-githook](https://github.com/aydabd/mamba-githook?tab=readme-ov-file#installation)
3. Initiate mamba-githook, check the installation link above
4. Create a new branch (e.g. `git checkout -b feature`)
5. Make your changes
6. Commit your changes (e.g. `git commit -am 'Add new feature'`)
7. Push to the branch (e.g. `git push origin feature`)
8. Create a new Pull Request


Testing
=======

Pre-commit hooks are used to run tests before each commit. To run the tests manually, use the following command:

.. code-block:: bash
    
    # Create a virtual environment
    python -m venv .venv
    pip install hatch
    # Run the tests
    hatch run test:all
    # For formatting
    hatch fmt


License
=======

This project is licensed under the MIT License. See the `LICENSE`_ file for details.

Contributing
============

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

Contact
=======

For any questions or suggestions, please open an issue on the GitHub repository.

.. _LICENSE: LICENSE
.. _compose.yaml: compose.yaml

