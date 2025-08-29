.. DDD Framework documentation master file

Welcome to DDD Framework Documentation
=======================================

**Documentation Driven Development** - Applying TDD principles to documentation coverage.

.. image:: https://img.shields.io/badge/coverage-85%25-brightgreen
   :alt: Documentation Coverage

.. image:: https://img.shields.io/badge/tests-103%2F115-yellow
   :alt: Test Status

Overview
--------

DDD Framework revolutionizes maintenance handoffs by treating documentation as code. 
Just as Test-Driven Development ensures code quality through tests, DDD ensures 
maintenance readiness through measurable documentation coverage.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   quickstart
   installation
   concepts

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   cli
   extractors
   coverage
   configuration

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/modules
   api/ddd.artifact_extractors
   api/ddd.coverage
   api/ddd.specs

.. toctree::
   :maxdepth: 2
   :caption: Maintenance Runbooks

   runbooks/index
   runbooks/ansible
   runbooks/troubleshooting

Key Features
------------

* **Measurable Coverage**: 85% documentation coverage threshold
* **Auto-Extraction**: Automatically extract maintenance documentation from code
* **DAYLIGHT Dimensions**: Comprehensive coverage across 8 maintenance dimensions
* **TDD for Docs**: RED-GREEN-REFACTOR cycle for documentation

Quick Example
-------------

.. code-block:: bash

   # Measure documentation coverage
   ddd measure ./my-project

   # Assert coverage meets threshold
   ddd assert-coverage ./my-project --threshold 85

   # Generate maintenance runbooks
   ddd generate-docs ./my-project --output ./docs

The Problem We Solve
--------------------

Every day, operations teams inherit code they didn't write. At 2AM during an incident, they need:

* What permissions does this need?
* What can go wrong?
* How do I know if it's working?
* What does this depend on?

DDD automatically generates this critical maintenance documentation.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`