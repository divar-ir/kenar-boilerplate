
# Kenar Divar Django Boilerplate

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/circleci/build/github/username/boilerplate?token=1234567890abcdef)](https://circleci.com/gh/username/boilerplate)

A boilerplate Django project for creating Kenar Divar applications. This project aims to simplify the creation of Kenar Divar applications by handling OAuth and other boilerplate functionalities. Developers can easily customize OAuth scopes and use the provided features without needing a deep understanding of the underlying layers.

## Table of Contents

- [Project Overview](#project-overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Local Development](#local-development)
- [Application Structure](#application-structure)
  - [Addon App](#addon-app)
      - [Models](#models)
      - [Views](#views)
  - [Chat App](#chat-app)
      - [Models](#models-1)
      - [Views](#views-1)
  - [OAuth App](#oauth-app)
      - [Models](#models-2)
      - [Views](#views-2)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This Django boilerplate is designed for creating applications for Kenar Divar. It includes the setup for handling OAuth authentication, chat functionality, and addon management. The project uses the Kenar SDK Python module to simplify interactions with the Kenar API.

## Installation

### Prerequisites

- [Python >= 3.10](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)

### Steps

1. Fork and clone the repository:

   ```sh
   git clone https://github.com/<your_user_name>/kenar-boilerplate.git
   cd kenar-boilerplate
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database:

   ```sh
   # Replace the values with your actual database configuration
   export DATABASE_NAME=kenar
   export DATABASE_USER=postgres
   export DATABASE_PASSWORD=postgres
   export DATABASE_HOST=localhost
   export DATABASE_PORT=5432
   ```

4. Apply migrations:

   ```sh
   python manage.py migrate
   ```

5. Run the development server:

   ```sh
   python manage.py runserver
   ```

## Configuration

Ensure you have the following environment variables set for the project:

- `APP_HOST`: The domain for your application
- `DIVAR_IDENTIFICATION_KEY`: A field set in the Kenar Panel for the application, used in the `start_chat_session` header
- `KENAR_APP_SLUG`: Refer to Kenar SDK documentation
- `KENAR_API_KEY`: Refer to Kenar SDK documentation
- `KENAR_OAUTH_SECRET`: Refer to Kenar SDK documentation
- `DJANGO_SECRET_KEY`: Your Django secret key

Example `.env` file:

```env
DJANGO_SECRET_KEY=your_secret_key
APP_HOST=yourappdomain.com
DIVAR_IDENTIFICATION_KEY=your_divar_identification_key
KENAR_APP_SLUG=your_kenar_app_slug
KENAR_API_KEY=your_kenar_api_key
KENAR_OAUTH_SECRET=your_kenar_oauth_secret
DATABASE_NAME=kenar
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

## Local Development

This guide will help you set up and run your Django project using Docker Compose and Ngrok for local development purposes.

### Prerequisites

1. **Docker**: Ensure that Docker is installed on your machine.
2. **Ngrok Account**: Sign up for an Ngrok account [here](https://ngrok.com/) and obtain your Ngrok auth token.
3. **Ngrok Static Domain**: Obtain a static domain for your Ngrok setup.
4. **Kenar Development App**: Create a Development App in Kenar or edit your current app, and set the Ngrok static domain like this:

   ```yaml
   fallback_url: https://<YOUR_NGROK_DOMAIN>/addon/addon_oauth
   session_init_url: https://<YOUR_NGROK_DOMAIN>/chat/start_chat_session
   oauth_redirect_urls:
     - https://<YOUR_NGROK_DOMAIN>/oauth/callback
   ```

### Setting Up

1. **Copy the Docker Compose Template**: Rename `docker-compose.dev.template.yml` to `docker-compose.yml`.

   ```sh
   cp docker-compose.dev.template.yml docker-compose.yml
   ```
2. **Update Environment Variables**: Open the `docker-compose.yml` file and replace placeholders with your actual values.

   ```yaml
   version: "3.8"
   
   services:
     db:
       image: docker.arvancloud.ir/postgres:16.0
       container_name: db
       restart: always
       environment:
         POSTGRES_DB: <DB_NAME>
         POSTGRES_USER: <DB_USER>
         POSTGRES_PASSWORD: <DB_PASSWORD>
       volumes:
         - ./postgres-data/:/var/lib/postgresql/data/
   
     app:
       build:
         context: .
       command: ["/bin/bash", "/app/wait-for-it.sh", "db:5432", "--", "/app/run.sh"]
       container_name: app
       restart: always
       depends_on:
         - db
       environment:
         DJANGO_SECRET_KEY: <RANDOM_SECRET>
         APP_HOST: <YOUR_NGROK_STATIC_DOMAIN>
         DIVAR_IDENTIFICATION_KEY: <YOUR_APP_IDENTIFICATION_KEY_IN_KENAR>
         KENAR_APP_SLUG: <YOUR_APP_SLUG>
         KENAR_API_KEY: <YOUR_APP_GENERATED_API_KEY_IN_KENAR>
         KENAR_OAUTH_SECRET: <YOUR_APP_OAUTH_SECRET_IN_KENAR>
         DATABASE_NAME: <DB_NAME>
         DATABASE_USER: <DB_USER>
         DATABASE_PASSWORD: <DB_PASSWORD>
         DATABASE_HOST: db
         DATABASE_PORT: 5432
       ports:
         - "8000:8000"
       volumes:
         - ./.:/app/
   
     ngrok:
       image: docker.arvancloud.ir/ngrok/ngrok
       container_name: ngrok
       command: ["http", "--domain=<YOUR_NGROK_STATIC_DOMAIN>", "8000"]
       network_mode: "host"
       environment:
         NGROK_AUTHTOKEN: <YOUR_NGROK_AUTH_TOKEN>
   ```

3. **Build and Run the Containers**: Use Docker Compose to build and start the containers.

   ```sh
   docker-compose up -d
   ```

### Components

- **db**: PostgreSQL database service.
- **app**: The Django application. It waits for the database to be ready before starting.
- **ngrok**: Ngrok service to expose your local server to the internet using a static domain. This is helpful when dealing with OAuth2.

### Environment Variables

- `APP_HOST`: Your Ngrok static domain.
- `NGROK_AUTHTOKEN`: Your Ngrok auth token.

### Running the Application

1. **Database Initialization**: The app service will automatically wait for the database to be ready before running any commands.
2. **Ngrok Tunnel**: The Ngrok service will expose your Django app running on port 8000 to the internet using the specified static domain.

### Accessing the Application

- **Local Access**: Open a browser and go to `http://localhost:8000/`.
- **Remote Access through Ngrok**: Open a browser and go to your specified Ngrok domain set in `APP_HOST`.

### Troubleshooting

- **Check Docker Logs**: Use the following command to check the logs of a specific service (e.g., the app service):

  ```sh
  docker-compose logs app
  ```

- **Stopping the Services**: To stop the services, use:

  ```sh
  docker-compose down -v
  ```

### Notes

- This setup is intended for local development. Using Ngrok with a static domain allows you to expose your local development server to the internet, making it easier to test webhooks or share your work with others.
- Ensure you have set the correct static domain and authenticated Ngrok with your auth token for the setup to work.
## Application Structure

### URL Configuration

Configured in `urls.py` to include admin routes and apps (`addon`, `chat`, `oauth`).

### Addon App

#### Models

- **Post**: Represents a post in Divar with its unique token.


#### Views

- **`addon_oauth`**: Initiates OAuth for the addon. Uses `post_token` and `callback_url` from query parameters, creates or retrieves the associated `Post`, and redirects to the OAuth provider.
- **`addon_app`**: Handles addon functionality post-OAuth. Validates the state, retrieves related `OAuth` and `Post` objects, and processes the addon logic. Redirects to the callback URL after processing.

### Chat App

#### Models

- **Chat**: Represents a chat in the context of a post. Contains the `post`, `user_id`, `peer_id`, and enforces unique combinations for `post`, `user_id`, and `peer_id`.


#### Views

- **`start_chat_session`**: Handles initiation of a chat session. Extracts authentication and request data, validates the user, and creates or retrieves `Post` and `Chat`. Signs OAuth session data and responds with the URL for `chat_oauth`.
- **`chat_oauth`**: Manages the OAuth workflow, validates and unsigns the OAuth session, ensures the session is stored, and creates appropriate OAuth scopes. Redirects to the OAuth provider.
- **`chat_app`**: Finalizes the chat initiation. Validates the OAuth session and state, retrieves related `OAuth` and `Chat` objects, and implements the core chat logic. Redirects to callback URL after processing.
- **`receive_notify`**: Receives chat notifications from Divar. Validates the request and authorization, processes the notification, and forwards it to the appropriate handler.

### OAuth App

#### Models

- **OAuth**: Manages OAuth tokens and states associated with sessions. Contains fields for `session_id`, `access_token`, `refresh_token`, `expires_in`, `phone`, `post`, `chat`. Includes an `is_expired` method to check token expiry.

#### Views

- **`oauth_callback`**: Handles the OAuth callback. Validates the state and authorization code, exchanges the code for access token, updates the database with OAuth session details, and redirects based on session type (POST/CHAT). Implements error handling for HTTP and general exceptions.

## Environment Variables

Here are the environment variables required for the project:

- `APP_HOST`: The domain for your application.
- `DIVAR_IDENTIFICATION_KEY`: Used in the `start_chat_session` header.
- `KENAR_APP_SLUG`: [Kenar SDK Readme](https://github.com/divar-ir/kenar-api?tab=readme-ov-file#kenar-api)
- `KENAR_API_KEY`: [Kenar SDK Readme](https://github.com/divar-ir/kenar-api?tab=readme-ov-file#kenar-api)
- `KENAR_OAUTH_SECRET`: [Kenar SDK Readme](https://github.com/divar-ir/kenar-api?tab=readme-ov-file#kenar-api)
- `DJANGO_SECRET_KEY`: Your Django secret key.
- `DATABASE_NAME`: The name of your PostgreSQL database.
- `DATABASE_USER`: The PostgreSQL database user.
- `DATABASE_PASSWORD`: The PostgreSQL database user's password.
- `DATABASE_HOST`: The host of your PostgreSQL database.
- `DATABASE_PORT`: The port of your PostgreSQL database.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.
