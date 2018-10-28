# LibreHQ-wikis

This is a placeholder description that should be filled out.

# Running as standalone

Running as a standalone is only for development and testing.  This is meang
to be part of the larger [LibreHQ](https://github.com/OpenTechStrategies/librehq-core)
project.

## Dependencies

LibreHQ-wikis uses [`pipenv`](https://docs.pipenv.org/) to manage its dependencies.
There are various installation instructions in the documentation but the common
ones are:

* Using pip: `pip install pipenv`
* Using brew: `brew install pipenv`

Then run `pipenv` to get all the local dependencies (see the Pipfile for the
full list)

```
$ pipenv install
```

## Booting the application

Start the application by running flask from the project directory:

```
$ FLASK_APP=wikis pipenv run flask run
```

## Using the application

At this time, the test server will run on port 5000.  Navigate to
[http://localhost:5000/wikis/] to use this submodule.

# Running as a submodule

Follow the installation instructions at
[LibreHQ](https://github.com/OpenTechStrategies/librehq-core)
to run this project as a submodule of the greater LibreHQ site.
