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


1. App is connected to GitHub so a deploy to `master` will deploy to Heroku:

        git checkout master
        git push origin

2. View the build from Heroku's [Activity](https://dashboard.heroku.com/apps/ciaff-eventbrite-click/activity) page.


Useful Commands
---------------

    heroku logs --tail

    heroku ps

    heroku ps:scale web=1


Database
--------

* https://www.mlab.com/databases/heroku_h5cf0v6g 
* https://elements.heroku.com/addons/mongolab
* https://docs.mongodb.com/getting-started/python/
* https://cloud.mongodb.com - not using this 


Email
-----

* https://github.com/sendgrid/sendgrid-python


Notes
-----

* The folder structure is based on [Learn Python The Hard Way Exercise 46: A Project Skeleton](http://learnpythonthehardway.org/book/ex46.html).
* The build was configured to work with CircleCI via [Continuous Integration and Continuous Deployment with Python](https://circleci.com/docs/language-python/).


Resources
---------

The following resources were used (but not harmed) in the making of this program:

* https://github.com/valermor/nose2-tests-recipes - great nose2 examples
* https://discuss.circleci.com/t/junit-reporting-with-nose2/1601

To read
-------

* https://circleci.com/docs/continuous-deployment-with-heroku/
* `virtualenvwrapper` - worth looking into.
