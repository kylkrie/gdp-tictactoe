# TicTacToe

I chose to build tictactoe using fastapi and angular to show that I'll be able to contribute despite not having much experience with these technologies. I hope to show that my system/api design standards and experience will carry over. 

## Table of Contents

- [Installation](#installation)
- [Development Setup](#development-setup)
- [Production Setup](#production-setup)
- [Usage](#usage)

## Installation

1. Clone the repo:
```sh
git clone https://github.com/kylkrie/gdp-tictactoe.git
```
2. Change to the project directory:
```sh
cd gdp-tictactoe
```
3. use docker compose to run the project in either [dev](#development-setup) or [prod](#production-setup) configuration

## Development Setup

For active development. Runs services with development config, watches files, hot reloads on code changes

```sh
docker compose up --build
```

## Production Setup

This provides a way of testing the production build flow. Issues with production specific configs, or bundling/copying static assets can happen for example.
Uses nginx to serve the website, this is so the production flow can be tested locally for the purpose of this exercise. For actual production I would have a CICD flow to build and upload to S3 behind a CDN like Cloudfront or Cloudfront. This removes the need to manage an nginx server.

```sh
docker compose -f docker-compose.prod.yml up --build
```

## Usage

app usage instructions
