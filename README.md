
# Kenar Divar Django Boilerplate

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/circleci/build/github/username/boilerplate?token=1234567890abcdef)](https://circleci.com/gh/username/boilerplate)

A boilerplate Django project for creating Kenar Divar applications. This project aims to simplify the creation of Kenar Divar applications by handling OAuth and other boilerplate functionalities. Developers can easily customize OAuth scopes and use the provided features without needing a deep understanding of the underlying layers.

## Table of Contents

- [Project Overview](#project-overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
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

1. Clone the repository:

   ```sh
   git clone https://github.com/username/boilerplate.git
   cd boilerplate
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database:

   ```sh
   # Replace the values with your actual database configuration
   export DATABASE_NAME=kenar_new
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
DATABASE_NAME=kenar_new
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

## Running the Project

1. Start the development server:

   ```sh
   python manage.py runserver
   ```

2. Open your browser and navigate to `http://127.0.0.1:8000/`.

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
