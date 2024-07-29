==================
open_producten
==================

:Version: 0.1.0
:Source: https://github.com/maykinmedia/open-producten
:Keywords: ``<keywords>``

|docs| |docker|

``<oneliner describing the project>``
(`Nederlandse versie`_)

Developed by `Maykin B.V.`_ for ``<client>``.


Introduction
============

``<describe the project in a few paragraphs and briefly mention the features>``


API specification
=================

|lint-oas| |generate-sdks| |generate-postman-collection|

==============  ==============  =============================
Version         Release date    API specification
==============  ==============  =============================
latest          n/a             `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/open-producten/main/src/open_producten/api/openapi.yaml>`_,
                                `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/open-producten/main/src/open_producten/api/openapi.yaml>`_,
                                (`diff <https://github.com/maykinmedia/open-producten/compare/0.1.0..main#diff-b9c28fec6c3f3fa5cff870d24601d6ab7027520f3b084cc767aefd258cb8c40a>`_)
0.1.0           YYYY-MM-DD      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/open-producten/0.1.0/src/open_producten/api/openapi.yaml>`_,
                                `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/open-producten/0.1.0/src/open_producten/api/openapi.yaml>`_
==============  ==============  =============================


See: `All versions and changes <https://github.com/maykinmedia/open-producten/blob/main/CHANGELOG.rst>`_


Developers
==========

|build-status| |coverage| |black| |docker| |python-versions|

This repository contains the source code for open_producten. To quickly
get started, we recommend using the Docker image. You can also build the
project from the source code. For this, please look at
`INSTALL.rst <INSTALL.rst>`_.

Quickstart
----------

1. Download and run open_producten:

   .. code:: bash

      $ wget https://raw.githubusercontent.com/maykinmedia/open-producten/main/docker-compose.yml
      $ docker-compose up -d --no-build
      $ docker-compose exec web src/manage.py loaddata demodata
      $ docker-compose exec web src/manage.py createsuperuser

2. In the browser, navigate to ``http://localhost:8000/`` to access the admin
   and the API.


References
==========

* `Documentation <https://TODO>`_
* `Docker image <https://hub.docker.com/r/maykinmedia/open-producten>`_
* `Issues <https://github.com/maykinmedia/open-producten/issues>`_
* `Code <https://github.com/maykinmedia/open-producten>`_
* `Community <https://TODO>`_


License
=======

Copyright © Maykin 2024

Licensed under the EUPL_


.. _`Nederlandse versie`: README.rst

.. _`Maykin B.V.`: https://www.maykinmedia.nl

.. _`EUPL`: LICENSE.md

.. |build-status| image:: https://github.com/maykinmedia/open-producten/workflows/ci/badge.svg?branch=main
    :alt: Build status
    :target: https://github.com/maykinmedia/open-producten/actions?query=workflow%3Aci

.. |docs| image:: https://readthedocs.org/projects/open-producten/badge/?version=latest
    :target: https://open-producten.readthedocs.io/
    :alt: Documentation Status

.. |coverage| image:: https://codecov.io/github/maykinmedia/open-roducten/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage
    :target: https://codecov.io/gh/maykinmedia/open-producten

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style
    :target: https://github.com/psf/black

.. |docker| image:: https://img.shields.io/docker/v/maykinmedia/open-producten?sort=semver
    :alt: Docker image
    :target: https://hub.docker.com/r/maykinmedia/open-producten

.. |python-versions| image:: https://img.shields.io/badge/python-3.11%2B-blue.svg
    :alt: Supported Python version

.. |lint-oas| image:: https://github.com/maykinmedia/open-producten/workflows/lint-oas/badge.svg
    :alt: Lint OAS
    :target: https://github.com/maykinmedia/open-producten/actions?query=workflow%3Alint-oas

.. |generate-sdks| image:: https://github.com/maykinmedia/open-producten/workflows/generate-sdks/badge.svg
    :alt: Generate SDKs
    :target: https://github.com/maykinmedia/open-producten/actions?query=workflow%3Agenerate-sdks

.. |generate-postman-collection| image:: https://github.com/maykinmedia/open-producten/workflows/generate-postman-collection/badge.svg
    :alt: Generate Postman collection
    :target: https://github.com/maykinmedia/open-producten/actions?query=workflow%3Agenerate-postman-collection
