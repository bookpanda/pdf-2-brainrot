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
- Prettier VSCode extension (also set format on save)


## Setup

1. Clone the repository
2. Run `pnpm install`
3. Copy `.env.template` file in root of the project as `.env` into the root of the project fill in the values (in discord).
4. If you want to use local databse, run `docker-compose up` to start it (you need to have Docker Desktop running, and you can use the default values in `.env.template` for the database connection)
5. Run `npx prisma migrate deploy` to create tables in the database
6. Run `npx prisma generate` to generate the Prisma client
7. Run `npx prisma db seed` to seed the database
8. Run `pnpm dev` to start the application

## Running E2E Tests

Some tests may mutate the database, it's expected to run only once on a freshly seed database.

1. Run `docker compose -f docker-compose.e2e.yaml up -d` to start new database for e2e test.
2. Run the following command to configure access for minio (S3 compatible storage)

```bash
docker exec e2e_s3 mc alias set e2e http://localhost:9000 admin password
docker exec e2e_s3 mc mb e2e/bookbook
docker exec e2e_s3 mc anonymous set public e2e/bookbook
```

3. Run `pnpm prisma migrate deploy` to migrate database.
4. Run `pnpm prisma db seed` to seed the database.
5. Run `pnpm e2e` to execute the tests.
6. Run `docker compose -f docker-compose.e2e.yaml down` to stop the database and delete all the data.

Repeat the steps to run E2E tests again.

You can also use `prepare-e2e.bash` which is step 1 to 4, note that it will delete `.env` file so make sure you save that in other name.

ts-node ./node_modules/@cucumber/cucumber/bin/cucumber-js ./tests/features/**/\*.feature --require ./tests/features/**/\*.ts

![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/seg-org/bookbook?utm_source=oss&utm_medium=github&utm_campaign=seg-org%2Fbookbook&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)