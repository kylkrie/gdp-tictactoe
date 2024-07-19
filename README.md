# TicTacToe

A TicTacToe project, with game logic in the backend and a simple web frontend.

I chose to build tictactoe using fastapi and angular to show that I'll be able to contribute despite not having much experience with these technologies.

I could've added more features like keeping score, a leaderboard, or game history but the task was just tictactoe. I decided to make a basic but solid tictactoe with good architecture, some basic auth, database connection, error handling, and a good local dev and prod setup to show experience with these concepts. It could still use some structured logging, docstrings, openapi docs setup, e2e tests but I think this is a good place to stop.

Concepts:
- Models: business logic. tictactoe game rules and actions.
- Stores: persistance layer. save and load models, abstracts database interactions.
- Services: higher level app logic, coordinates models and stores.
- API/Routes: interface layer, exposes service functionality, handles http request/response and dtos.

Asyncpg and raw SQL over an ORM
- I like to keep things simple. An ORM intruduces more dependencies and libraries to learn
- Not a fan of "magic", I like knowing and having control of the actual SQL statements being run
- Added a simple migrations script, if rollbacks or anything more complicated is needed, could warrant using a library

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Development Setup](#development-setup)
- [Production Setup](#production-setup)
- [Usage](#usage)

## Prerequisites

- Docker and Docker Compose
- For local development:
  - Python 3.9
  - Node.js and npm (I'm on v18.15.0, not sure what min version would be)

## Installation

1. Clone the repo:
```sh
git clone https://github.com/kylkrie/gdp-tictactoe.git
```
2. Change to the project directory:
```sh
cd gdp-tictactoe
```
3. Use docker compose to run the project in either [dev](#development-setup) or [prod](#production-setup) configuration

## Development Setup

For active development. Runs services with development config, watches files, hot reloads on code changes.

Using docker allows everyone to run in the same dev environment. And can setup multiple services and dependencies like databases.

```sh
docker compose up --build
```

That's all you need to run the project. For local dev, you'll still need to install packages for code completion and references in your IDE
```sh
cd api-service
python -m venv venv
pip install -r requirements.txt
cd ../angular-app
npm install
```
Tests can be run locally with pytest
```sh
cd api-service
pytest
```

## Production Setup

This provides a way of testing the production build flow. Issues with production specific configs, or bundling/copying static assets can happen for example.
Uses nginx to serve the website, this is so the production flow can be tested locally for the purpose of this exercise. For actual production I would have a CICD flow to build and upload to S3 behind a CDN like Cloudfront or Cloudflare. This removes the need to manage an nginx server.

Tests are run before the api service starts up in prod. They could be run in a pre-commit git hook, but I like them in a CI flow so they're run in a consistent environment and don't take up dev time. I don't have a CI flow so I at least made them run before the prod service starts up.

```sh
docker compose -f docker-compose.prod.yml up --build
```

## Usage

Once the docker containers are running, go to [http://localhost:4200](http://localhost:4200)

Game Rules:
- X always goes first
- The player is randomly assigned X or O for each new game
- Click on an empty cell to make a move
- Computer will make a follow up move
- The game ends when a player gets three in a row (horizontally, vertically, or diagonally) or when all cells are filled (a tie)
- Use the "New Game" button to start a new game at any time
