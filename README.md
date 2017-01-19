# Goodnight LEAD Lab

Authors: Eric Horton, Sam Magura (śȑmȧgũŗa@ncsu.edu)   
License: GPL

LEAD Lab is a web application that lets users answer psychological questionnaires to learn more about themselves. It was developed for use in leadership training seminars run by Goodnight Scholars Program at NC State University.

LEAD Lab is written in Python and built on top of the Django web framework. The project uses PostgreSQL and is designed to be deployed on Heroku.

## Feature overview
* **Psychological inventories:** LEAD Lab allows users to fill out and view the results of six different psychological questionnaries, including the Big Five personality test. The results are displayed graphically to make it easy to interpret the results in the context of the general population:

<img src="https://cloud.githubusercontent.com/assets/801549/22111301/db6e665c-de2c-11e6-9c9f-276a781e3cec.png" width="450" />

* **Statistics:** LEAD Lab reports basic statistics on the aggregated results of the psychological inventories, with the option to download the raw data in Excel and JSON formats.

<img src="https://cloud.githubusercontent.com/assets/801549/22111557/a95d2094-de2d-11e6-9014-0a872323a09b.png" width="600" />

* **Organizations and sessions:** The organization and session objects are used to group users appropriately. To understand this feature, we need to talk about how LEAD Lab is used in practice. An *organization* (e.g. the Goodnight Scholars Program) is going to run a leadership seminar. They create a *session* representing that specific group of users (e.g. Fall 2017 Development Seminar). Then the site generates a registration URL that users in that session can enter to reach the registration page.

<img src="https://cloud.githubusercontent.com/assets/801549/22111615/e8f9d2e2-de2d-11e6-8a58-94f41ca84cf8.png" width="1000" />

* **User demographics:** When users register, they are asked to supply a variety of demographic information, which is used in the data analytics.

<img src="https://cloud.githubusercontent.com/assets/801549/22111638/067808fc-de2e-11e6-97a0-a3426701c9be.png" width="800" />

* **Django admin site:** All administrative tasks are performed via the Django admin site.

* **Customizable dashboard:** In particular, the admin site can be used to edit the HTML content displayed on the dashboard via a WYSIWYG editor.

<img src="https://cloud.githubusercontent.com/assets/801549/22111670/21b03d7e-de2e-11e6-8685-e91a11617432.png" width="800" />

* **Mobile-first responsive design:** The client originally wanted LEAD Lab to be a mobile app. But native mobile apps take a lot of effort to develop, since the developer has to create separate versions for iOS and Android. And if you want to use the application on your desktop computer, you're out of luck. Instead, we choose to make LEAD Lab a web application with a responsive layout that scales to fit the user's screen. With the help of the Bootstrap CSS library, we are able to deliver a site that looks great on phones, tablets, and PC's, all with the same HTML. 

The organization and design of LEAD Lab follows the standard conventions for Django projects. The main source code is in the `gl_site` directory. The directory `gl_site/test` contains unit tests for all of the main features.

## Development and administration information
The [GitHub Wiki](https://github.com/srmagura/goodnight-lead/wiki) contains guides on deployment, administration, and development of the project.
