# Terraform FastAPI Backend

This project implements a custom HTTP backend for Terraform using FastAPI. It provides endpoints for state management and locking, allowing Terraform to store and retrieve state information, as well as implement state locking for concurrent operations.

## Features

- Store and retrieve Terraform state
- Implement state locking mechanism
- Compatible with Terraform's HTTP backend

## Requirements

see [requirements.txt](requirements.txt)

## Installation

1. Clone this repository:

```bash
git clone git@github.com:mikelv702/simple-terraform-backend.git
```

2. Install the required packages:

```bash
uv pip install -r requirements.txt
```

## Usage

1. Start the FastAPI server:

```bash
cd src/
fastapi dev main.py
```

2. Configure Terraform to use this backend:

```hcl
terraform {
  backend "http" {
    address = "http://localhost:8000/tfstate"
    lock_address = "http://localhost:8000/tfstate/lock"
    unlock_address = "http://localhost:8000/tfstate/lock"
  }
}
```

3. Use Terraform as normal. The state will be stored and retrieved from your FastAPI backend.

## API ENDPOINTS 

- POST /tfstate: Update Terraform state
- GET /tfstate: Retrieve Terraform state
- LOCK /tfstate/lock: Acquire a state lock
- UNLOCK /tfstate/lock: Release a state lock
- GET /tfstate/lock: Retrieve current lock info

## Note

This is a basic implementation and should not be used in production without further security measures and persistent storage solutions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.