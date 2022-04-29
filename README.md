## TASK ASSIGNMENT AND SCHEDULER API

- This restapi solves the problem of complex task assignment to peers
- It can be used as personal scheduling app for reminder
- Main motive behind this web-app is to collectively send mails about event reminder or deadline reminder of a
  particular group
- The groups can be various clubs in an institutions or different teams in a company, etc

## ROUTES TO IMPLEMENT

| METHOD   | ROUTE                            | FUNCTIONALITY                                        | ACCESS      |
|----------|----------------------------------|------------------------------------------------------|-------------|
| *POST*   | ```/auth/signup```               | _Register new user_                                  | _All users_ |
| *POST*   | ```/auth/login```                | _Login user_                                         | _All users_ |
| *POST*   | ```/task/register_club```        | _Register for a club_                                | _All users_ |
| *GET*    | ```/task/all_users```            | _See details of all users_                           | _Superuser_ |
| *GET*    | ```/task/user/{id}```            | _See details selective users_                        | _Superuser_ |
| *GET*    | ```/task/user_clubs```           | _See logged in user details_                         | _All users_ |
| *DELETE* | ```/task/unregister_club/{id}``` | _Unregister from the club_                           | _All users_ |
| *PATCH*  | ```/task/update_profile/{id}```  | _Update the current user to superuser or vice-versa_ | _Superuser_ |
| *POST*   | ```/mail/personal_reminder```    | _Set up personal reminder_                           | _All users_ |
| *POST*   | ```/mail/club_mail```            | _Set up club meetings and schedule events_           | _Superuser_ |
| *GET*    | ```/docs/```                     | _View API documentation_                             | _All users_ |

## How to run the Project

- Install Postgreql
- Install Python
- Git clone the project with ``` git clone https://github.com/sanial2001/RESTAPI_task_scheduler.git```
- Create your virtualenv with `Pipenv` or `virtualenv` and activate it.
- Install the requirements with ``` pip install -r requirements.txt ```
- Set Up your PostgreSQL database and set its URI in your ```db.py```
- Create .env file to store the credentials regarding your database and email id and password
```
SQL_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
```
- Finally, run the API
``` uvicorn app.main:app --reload```
