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

## Usage
* Install pipenv
* pipenv shell
* Run main.py with command line arguements -c, -t, -n and bills
* Example: python3 main.py -c 116 -t sjres -n 1 bills
    - the -c command specifies a congress
    - the -t command specifies an object type
    - the -n command specifies a number
    - bills specifies the pipe to be run
    - The pipe will crank and save to a local db.

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
* Add file output for capturing and storing raw input?