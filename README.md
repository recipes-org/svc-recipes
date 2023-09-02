## Broad plan

- basically ~~3~~ n services
    - measurements
    - ingredients
    - recipes
    - (users)
    - (images)
    - (search)
    - (suggestions)
    - (front end(s))
- users
    - [JWT](https://fastapi.tiangolo.com/tutorial/security/)
    - login with ...
    - [Discussion](https://github.com/tiangolo/fastapi/issues/12)
    - [Tutorial](https://intility.github.io/fastapi-azure-auth/)
    - instagram - source of many recipes

- trace and span IDs

- hosting

## Things I actually want

- async wsgi runner / http layer handler e.g. `uvicorn`
- routing
- db interaction - but not necessarily ORM
    - migrations likely nice

~~Pydantic and ORMs are difficult - better to follow the FastAPI [official docs](https://fastapi.tiangolo.com/tutorial/sql-databases/#review-all-the-files).~~

... Although that appears to be changing soon.

## FastAPI

FastAPI provides pretty handy (de)serialisation and corresponding http error responses.

... But that isn't the end of the world to implement.

... And it seemed I had to implement this myself basically anyway.
Since you have to do this between the Pydantic and SQLAlchemy models.
Unless you buy into sending the ORM models all the way back up to the
router response models for Pydantic to handle it.
But that means you can't split out any of those layers from the ORM.
E.g. repository, unit of work, service, ...

Dependency injection is cool (I guess) and probably would be a pain to implement.

... But what is the point of it?

## SQLAlchemy

SQLAlchemy ORM is pretty cool.

... But it isn't _required_ to make something useful.

## SQLModel

MOAR convenience.

... But MOAR opinions and based on < v2 for both of the above.

Seems like convenience that is good for CRUD-based things.
