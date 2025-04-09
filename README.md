# goit-pythonweb-hw-08

#### 1. Creating and connecting to a database
In this work, we will use a postgres database.

Make sure you have the PostgreSQL server running and the database specified in the ```.env``` file created.

At the command line, start the Docker container:

```bash
docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```
Instead of ```some-postgres```, choose your container name, and instead of ```mysecretpassword```, come up with your password to connect to the database.

SQLAlchemy will automatically create the ```contacts``` table the first time the API is run thanks to the line in the ```main.py``` file:
```python
database.Base.metadata.create_all(bind=database.engine)
```
Creating a "contacts" database in PostgreSQL:
1. Go to the PostgreSQL Docker container:
```bash
docker exec -it contacts bash
```
2. Switch to the ```name``` user, for example, ```postgres```:
```bash
su postgres
```
3. Start the ```psql``` client:
```bash
psql
```
You should see the command line ```postgres=#```.
4. Create the "contacts" database:
```sql
CREATE DATABASE contacts;
```
5. Check the list of existing databases:
```sql
\l
```
6. Exit ```psql``` and the container:
```sql
\q
exit
exit
```

#### 2. Запуск API
Make sure you are in the root directory of the project (where the ```main.py``` file is located) and run the API using Uvicorn:
```
uvicorn main:app --reload
```
Once launched, you will be able to access the Swagger documentation at ```http://127.0.0.1:8000/docs``` or ```http://127.0.0.1:8000/redoc```.

#### API Functionality Overview
- POST /contacts/: Create a new contact. Expects a JSON request body with contact data.
- GET /contacts/: Get a list of all contacts. Supports pagination using ```skip``` and ```limit``` parameters, as well as filtering by ```first_name```, ```last_name```, and ```email``` via query parameters.
- GET /contacts/{contact_id}: Get a single contact by its ID.
- PUT /contacts/{contact_id}: Update an existing contact by its ID. Expects a JSON request body with updated data.
- DELETE /contacts/{contact_id}: Delete a contact by its ID.
- GET /contacts/birthdays/upcoming: Get a list of contacts with a birthday in the next 7 days.

#### Packages
- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary
- python-dotenv
- pydantic