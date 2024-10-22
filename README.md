# wolt assignment

## architecture
I chose Python with Flask to create the API because it is a quick and easy stack to create an API with. Python is dynamically typed, interpreted and can be easy and fast to work with, especially in the case of a small API like this one. Flask is one of the go-to frameworks for creating a REST API in Python, besides Django and FastAPI, I chose Flask specifically because I am most familiar with it.

### data storage & infrastructure
To store the Users and Messages, I chose to Postgres database instance. While this isn't particularly a "lightweight" instance, I chose to execute this assignment this way to assure it is easy to reproduce. The API is dockerized, and the docker-compose file pulls up the Postgres database in the same cluster, allowing seamless communication.

### data access
The data is accessed via SQLAlchemy, a popular ORM in Python. The models are defined under repository, with some metadata about the relationship between the two models (User and Message). SQLAlchemy then does the "heavy lifting" allowing the business logic to be short and concise.

### code structure
The API code is structured under the /src folder, which is conventional in most languages. Under /src, you will find /repository and a /services folders. Repository handles the ORM code, the models, while services contain stateless services which contain business logic for the API.
Routes are defined in the routes.py module. Routes could also be a separate folder, with individual modules for related APIs, but I chose to keep it simple in this case.

### API routes
The routes themselves are quite straight forward, I had one main design standard in mind when creating them, and that is the CRUD design of a typical REST API. Because of this, User objects can be accessed via GET /users, if an email query param is added, it is filtered to users with that given email. DELETE, POST and PUT are implemented similarly as POST /users/, PUT /users/{id} and DELETE /users/{id}

## Tests

Unit tests for the business logic was added (User service, Message service) as this was the main body of code.
There could be additional levels of testing, but at this size this is the extent I feel necessary.