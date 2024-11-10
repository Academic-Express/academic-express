# academic-express

## Pre-requisites

- Python 3.12 or later
- Node.js 18 or later
- Docker with Docker Compose (for deployment)

## Development

1. Clone the repository.

2. Follow the instructions in [backend/README.md](backend/README.md) and [frontend/README.md](frontend/README.md) to set up the backend and frontend respectively.

## Deployment

1. Clone the repository.

2. Create a `.env` file:

   ```sh
   cp .env.example .env
   ```

   Optionally, you can change the values in the `.env` file. For example, you can change the `PIP_EXTRA_ARGS` variable to provide additional arguments to `pip install`, e.g. `--index-url <some-pip-mirror> --trusted-host <some-host>`.

3. Generate secrets for the backend:

   ```sh
   bash generate_secrets.sh
   ```

   This will generate files in the `secrets/` directory.

4. Build and run the application:

   ```sh
   docker compose up --build
   ```

   The website will be available at `http://localhost:80`. Use the `-d` flag to run in detached mode.
