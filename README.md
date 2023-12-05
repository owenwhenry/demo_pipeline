# demo_pipeline

This is a quickie sample repo to talk about my understanding of how to best 
build data pipelines in Python. Starting from a single command line script as a
common interface, it then can branch into any number of pipelines flexibly and
extensibly. 

Part of the idea here is to encode any assumptions I have about the form and 
shape of the data in Pydantic, and use the resulting model to validate any item 
I receive from an external source as part of the loading process. I find this 
beneficial because it catches errors with your data as far upstream as possible.

## Quick tour
* main.py is where the command line utility lives.
* schemas.py holds the pydantic definitions
* Files under database deal with connections to storage - assumed to be a db
* In pipelines you have various data obj's and clients, leveraging inheritance

## Why Pydantic?
* Serves as built-in documentation of what form data is expected in
* Provides type hints as you're working with the models
* Allows you to build in custom validation against each item you're processing

## Why SQLAlchemy?
* In Python code, I'd rather work with the ORM than raw SQL (it's prettier)

# TODO
* Add tests
* Futz with logging messages and levels throughout
* Containerize this?