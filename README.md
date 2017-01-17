# Goodnight LEAD Lab

Authors: Eric Horton, Sam Magura (śȑmȧgũŗa@ncsu.edu)
License: GPL

LEAD Lab is a web application that lets users answer psychological questionnaires to learn more about themselves. It was developed for use in leadership training seminars run by Goodnight Scholars Program at NC State University.

LEAD Lab is written in Python and built on top of the Django web framework. The project is designed to be deployed on Heroku, and as such uses PostgreSQL.

## Feature overview
* **Psychological inventories:** LEAD Lab allows users to fill out and view the results of six different psychological questionnaries, including the Big Five personality test. The results are displayed graphically to make it easy to interpret the results in the context of the general population:
[image of results]

* **Statistics:** LEAD Lab reports basic statistics on the aggregated results of the psychological inventories, with the option to download the raw data in Excel and JSON formats.
[image]

* **Organizations and sessions:** The organization and session objects are used to group users appropriately. To understand this feature, we need to talk about how LEAD Lab is used in practice. An *organization* (e.g. the Goodnight Scholars Program) is going to run a leadership seminar. They create a *session* representing that specific group of users (e.g. Fall 2017 Development Seminar).
[image of admin site page]

* **User demographics:** When users register, they are asked to supply a variety of demographic information, which is used in the data analytics.
[image of registration page]

* **Django admin site:** All administrative tasks are performed via the Django admin site.

## Development and administration information
The [GitHub Wiki](https://github.com/srmagura/goodnight-lead/wiki) contains guides on deployment, administration, and development of the project.
