# Dashboard Documentation

**NOTE** Environment variables need to be set before running the app. This should be saved to `./.env`. Please seee the `./example_env` on the format to use and variables to set.

**To use any of the python code in this application, the dependencies defined in the requirements.txt file should be installed `pip install -r requirements.txt`. For some reason, the package `psycopg2` AND `psycopg2-binary` was required for the scripts and database migrations, but only `psycopg2-binary` could be installed in the Docker containers. If you have problems in running any of the scripts outside of Docker, you may need to install `psycopg2`, but do not add this to the `requirements.txt` file as this cannot be installed in Docker. This application was written using `Python 3.11.3`**

The dashboard frontend and backend are all launched and linked together using Docker and docker-compose (you will need to install these on your computer for this to work). To run the full application, `cd` to the current location in your terminal and run `docker-compose up -d --build` (omit the `-d` to run the application log messages to the terminal). Any changes made to the code will not be reflected in the running app, and the app will need to be stopped and rebuilt for changes to take effect. 

After the app has started and the tables inserted into the database, the frontend can be accessed from `http://127.0.0.1/` and the API documentation/sandbox from `http://localhost:8000/api/ui/` - in this Swagger UI, you can see how queries can be built using different parameters, and test queries with different inputs.

**Before running the app for the first time, tables will need to be generated for the database. See Part 2 below in *Running the API app locally***

## API and Database
The API follows [OpenAPI specification](https://www.openapis.org/). The apps routes/endpoints are defined in the `api/app/api-config.yaml`, with an element for each endpoint. The `operationId` in the `yaml` file points to the python functions that process the queries, all defined in `api/app/endpoints.py`. Before querying the data, all of the parameters are validated through `api.app.data_access.validate_params`, with each of the parameters' validation and datatype defined in `api/app/data_types.py`. Once the requests have passed validation, the queries are passed to their corresponding functions in `api/app/data_queries.py` (sometimes via `api/app/data_access.py`) to be queried by the database.\
PDF reports are generated in `api/app/generage_pdf_report.py`.

### Running the API app locally
The API/database can be run independently from the front-end for testing/debugging purposes. Changes made to the app when running it in this way will be reflected in the running app without having to restart it. As data is not persisted in the database container, the following steps will need to be followed to start the app and populate the database.
1. Start the database container:\
`cd` to `./api/scripts/postgres_local_dev` and run `docker-compose up -d –build`
2. Prepare the tables for the database (this only needs to be done once per table version. If tables change, this will need to be re-run):\
`cd` back to the api root `./api/` and run `python scripts/reformat_csvs_for_db.py`. This will also create the tables used in the unit tests. For this to work, you will need to have your `enriched_ref_ics_data.csv` table saved to `/ICS_Analysis/data/enriched/` (this ignored by `Git`). This script will make all the tables required for the database, but because of its size, the `ICS_DATABASE_TABLE.csv` will also be ignored by `Git`, but it can be left in its location. 
3. Insert the tables to the database:\
From the same directory, run `python scripts/insert_data.py`. This script will create the database schema and insert the tables to the database. This script will fail if the `csv` tables are changed to differ from the database schema. To change the schema, see *Database migrations*
4. Run the app in debug mode:\
`python ./wsgi.py`
**The `api/app/data/db-data/WEBSITE_TEXT.csv` holds text and colourramps to be used in the frontend. Please edit this table to make changes to the frontend. Please do not add fields to this table until you have read *Database migrations* below.**

### Database migrations - only required if changes made to DB Schema
The application uses `alembic` [https://alembic.sqlalchemy.org/en/latest/](https://alembic.sqlalchemy.org/en/latest/) to apply version control to changes to the database schema. This process only needs to be followed when tables schemas or their fields' data-types change. The database schema is defined in `api/app/models.py`, with a model class for each table. A database should be running (from either of the docker-compose lines mentioned above) for the following process to work.
1. Set the database credentials in `alembic.ini`:\
This cannot be set via the environment variables in line 63 so it needs to be hardcoded `sqlalchemy.url = postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/ics` **and reset following the migration**.
2. Make the migration file:\
Run `alembic revision --autogenerate -m "<Message-detailing-the-database-change>`
3. Migrate the change to the database:\
Run `alembic upgrade head`
**Data should then be added to the database through the `./scripts/insert_data.py` file - This may need editing based on the changes you have made to the database.

### Unit and end-to-end tests
Tests have been written to test the application's data queries and the endpoints using `pytest` [https://docs.pytest.org/en/7.4.x/](https://docs.pytest.org/en/7.4.x/). A test application and database are defined in `tests/conftest.py` with tables from `tests/test_data` being automatically inserted into the test database for the tests, which is torn down after the tests.\
All tests can be run by running `pytest tests --disable-warnings`

### Linting
Following any changes, linting can be run on the code through the following commands from within the `api` folder:\
1. `python -m black app`
2. `python -m flake8 app`
3. `python -m isort app`
4. `python -m mypy app`

## Frontend
