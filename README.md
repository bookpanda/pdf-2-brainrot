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
- `Black Formatter` VSCode extension (also set format on save, and set as default formatter for python in `settings.json`)

# Backend (/backend)

## Setup

1. Clone the repository
2. Run `poetry install` (to add packages do `poetry add <package>` and `poetry update` to update all packages)
3. Copy `.env.template` file in root of the folder as `.env` into the same directory fill in the values.
4. Run `poetry env activate` to activate the virtual environment
5. Run `poetry env info --path` to get the path of the virtual environment
6. In VSCode, `Ctrl + Shift + P` and type `Python: Select Interpreter`, select `Enter interpreter path...` and paste the path of the virtual environment. This will allow intellisense for the project
7. Run `poetry run python run.py` to start the application

# Frontend (/frontend)

## Setup
- like backend
- Run `poetry run streamlit run app.py` to start the application

## Tips
- Swagger is available at `http://localhost:8000/docs`
- If you don't want to see `__pycache__` folders, add this to VSCode's `settings.json` file:
```json
"files.exclude": {
    "**/__pycache__": true,
  },
``` 