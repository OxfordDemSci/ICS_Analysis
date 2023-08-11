# Dashboard Documentation

**NOTE** Environment variables need to be set before running the app. This should be saved to `./.env`. Please seee the `./example_env` on the format to use and variables to set.

The dashboard frontend and backend are all launched and linked together using Docker and docker-compose (you will need to install these on your computer for this to work). To run the full application, `cd` to the current location in your terminal and run `docker-compose up -d --build` (omit the `-d` to run the application with logging messages printed to the terminal). And changes made to the code will not be reflected in the running app, and the app will need to be stopped and rebuilt for changes to take effect. **Before running the app for the first time, tables will need to be generated for the database. See Part 2 below in *Running the API app locally***

## API and Database

### Running the API app locally
The API/database can be run independently of the front-end for testing/debugging purposes. Changes made to the app when running it in this way will be reflected in the running app without having to restart it. As data is not persisted in the database container, the following steps will need to be followed to start the app and populate the database.
1. Start the database container:\
`cd` to ./api/scripts/postgres_local_dev and run `docker-compose up -d –build`
2. Prepare the tables for the database (this only needs to be done once per table version. If tables change, this will need to be re-run):\
`cd` back to the api root `./api/` and run `python scripts/reformat_csvs_for_db.py`. This will also create the tables used in the unit tests.
3. Insert the tables to the database:\
From the same directory, run `python scripts/insert_data.py`. This script will create the database schema and insert the tables to the database. This script will fail if the `csv` tables are changed to differ from the database schema. To change the schema, see *Database migrations*
4. Run the app in debug mode:\
`python ./wsgi.py`
