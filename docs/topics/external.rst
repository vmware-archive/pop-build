=================
External Builders
=================

Pop-Build can be used to define a build without altering the target
application's source tree. This can be useful when building third
party applications.

All that needs to be done is to define a `run.py` as the entry script
and then to create a `requirements.txt` file that will include the
target application. To illustrate that this can be done with even a
very complicated software platform this example will build a single
binary of `Salt`, one of the largest python projects.
