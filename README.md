eventbrite-click
================

Generates a "click" - total of how many people are at an Eventbrite event.

Uses the [Flask](http://flask.pocoo.org/) web microframework.


Running it
----------

1. Ensure you have Python installed.
1. Generate your personal Eventbrite OAuth token.
1. Create `envvars.bash`: `cp envvars-example.bash envvars.bash`
1. Create a virtualenv:

        virtualenv .venv
        source .venv/bin/activate

1. Run the program:

        heroku local web


Deployment
----------

* https://devcenter.heroku.com/articles/getting-started-with-python
* https://dashboard.heroku.com/apps/ciaff-eventbrite-click


App is connected to GitHub so a deploy to `master` will deploy to Heroku:

        git checkout master
        git push origin

Useful Commands
---------------

    heroku logs --tail

    heroku ps

    heroku ps:scale web=1


Notes
-----

    virtualenvwrapper
