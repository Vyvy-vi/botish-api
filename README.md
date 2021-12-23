# Botish API

This is an API originaly made for the [Heptagram Bot](https://github.com/Heptagram-Bot/) project, now called labeled under the  [botish.xyz](https://api.botish.xyz/) domain, maintained by Vyvy-Vi.
For contributing to the project, check out the [CONTRIBUTING.md](./CONTRIBUTING.md) file.

## Features

_Coming soon..._


## Requirements

- `Python` v3.7+
- `fastapi` (API framework)
- `poetry` (dependency manager)
- `uvicorn` (ASGI server)
- `pip` (needed to install poetry)

## Setting up the dev environment

1. Install Poetry
   ```
   pip install poetry
   ```

2. Set up the project dependencies and the pre-commit hooks
   ```
   poetry install
   poetry run task precommit
   ```
3. Set up the MongoDB instance
   <!--#TODO: Fill more setup info here, after setting up the docker container-->

4. Run the project
   ```
   poetry run task start
   ```

5. Linting your code
   ```
   poetry run task lint
   ```
## Usage

<!--#TODO: Fill info about usage here, after the API is sorta ready-->
