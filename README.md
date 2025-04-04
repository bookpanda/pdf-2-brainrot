# pdf-2-brainrot

## Stack

- fastapi
- streamlit
- AWS: VPC, EC2, S3, DynamoDB, Polly, Textract
- terraform

## Prerequisites

Download these tools before you start working on the project.

- python 3.12
- poetry
- ngrok (for setting up a public endpoint of locahost for SNS webhook)
- `Black Formatter` VSCode extension (also set format on save, and set as default formatter for python in `settings.json`)

# Infrastructure (/infrastructure)

## Setup
1. Run `terraform init` to initialize the terraform project
2. Run `terraform plan` to see the changes that will be applied
3. Copy `.env.template` file in root of the folder as `.env` into the same directory fill in the values.
4. Run `ngrok http 8000`, copy the forwarding url (e.g. `https://8a24-49-228-104-201.ngrok-free.app`) and paste it in the `.env` in the field `SNS_TOPIC_ENDPOINT`
5. Run `chmod +x load_env.sh` to make the script executable
6. Run this to create the infrastructure
```bash
source ./load_env.sh
terraform apply
```
7. Run `terraform output -raw secret_access_key` to get the secret access key for `backend setup`

# Backend (/backend)

## Setup

1. Run `poetry install` (to add packages do `poetry add <package>` and `poetry update` to update all packages)
2. Copy `.env.template` file in root of the folder as `.env` into the same directory fill in the values.
3. Run `poetry env activate` to activate the virtual environment
4. Run `poetry env info --path` to get the path of the virtual environment
5. In VSCode, `Ctrl + Shift + P` and type `Python: Select Interpreter`, select `Enter interpreter path...` and paste the path of the virtual environment. This will allow intellisense for the project
6. Run `poetry run python run.py` to start the application

## .env
```bash
# these envs are available by doing terraform apply in /infrastructure
AWS_ACCESS_KEY_ID= # access_key_id
AWS_SECRET_ACCESS_KEY= # after applying, run `terraform output -raw secret_access_key`
AWS_REGION= # region
AWS_BUCKET_NAME= # bucket_name
```

# Frontend (/frontend)

## Setup
- like backend (skip step 2, 7)
- Run `poetry run streamlit run ./app/app.py` to start the application

## Tips
- Swagger is available at `http://localhost:8000/docs`
- If you don't want to see `__pycache__` folders, add this to VSCode's `settings.json` file:
```json
"files.exclude": {
    "**/__pycache__": true,
  },
``` 