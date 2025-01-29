# FreeRADIUS Admin Integrations

This directory contains integrations with other 3rd party services. Each integration functions via connecting to a 3rd party API and importing some devices into FreeRADIUS Admin.

## Adding a new integration

Each integration should inheret from the `BaseIntegration` class. This class provides a number of helper methods to make the integration easier to implement. Define the new class in the `models` directory and import it into `models/__init__.py`.