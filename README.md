# Astronomer Connection Types

Welcome! This repo documents Airflow connection types available to the Astro platform. To request a new one, [file a new issue](https://github.com/astronomer/airflow-connection-docs/issues/new).

# Principles for adding to this repository

The goal of this repository is to collect accurate and useful data for connecting to Airflow's Providers (eg. Snowflake, Google Bigquery, to name a few).

To add a new connection type for a provider, make a branch with changes to the connections/dev directory, adding or changing connection type data as needed. Please feel free to reference the "Snowflake" connection type for a reference of the schemas supported by this repository.

Next, open a draft pull request and check the CI jobs to ensure that validation suceeded on the metadata. Finally, mark the pull request as "ready for review" and someone on the team will review!
