# TicTacToe

A TicTacToe project, with game logic in the backend and a simple web frontend.

I chose to build tictactoe using fastapi and angular to show that I'll be able to contribute despite not having much experience with these technologies. I hope to show that my system/api design standards and experience will carry over. 

My main focus was on the backend, frontend is very simple just to be able to play.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Development Setup](#development-setup)
- [Production Setup](#production-setup)
- [Usage](#usage)

## Prerequisites

- Docker and Docker Compose
- For local development:
  - Python 3.9.19
  - Node.js and npm (I'm on v18.15.0)

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

## Production Setup

This provides a way of testing the production build flow. Issues with production specific configs, or bundling/copying static assets can happen for example.
Uses nginx to serve the website, this is so the production flow can be tested locally for the purpose of this exercise. For actual production I would have a CICD flow to build and upload to S3 behind a CDN like Cloudfront or Cloudflare. This removes the need to manage an nginx server.

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
