## Longitudinal:
longitudinal means collecting data from the same candidate to analyze how the candidate has improved over time. Eg: consider a university student who takes an exam every 3 months. We monitor him for 1 year and to do that we make this table:
Exam        Score       Remarks
Jan         40/100      Mistakes in sub ...
Apr         50/100      Improvement in ...
Jul         65/100      Scope of improvement in ...
Oct         90/100      Excellent performance

As we can see that we monitor the same student across different times to analyze his performance. This is called longitudinal data

## What we're building
a web based platform for managing longitudinal data for a hospital. The app will help doctors enroll patients, schedule visits, capture the study data and export the data as a dataset

## The problem my project solves
Clinical research teams often struggle with these problems and what my project solves:
1. Tracking participants across multiple visits over months and years
2. ensuring participant visits occurs within allowed time windows: in clinical trials, along with the actual testing day, the participant can also come on other days. For eg: consider the candidate has fever and the doctor has asked them to come on Jan 15th along with a window of -2/+2 days. This means the candidate can come any day from 13th (15-2) to 17th (15+2). This is done cuz on 15th the candidate may not be able to come due to high fever and he can come on other days. Also the window is given strategically as the fever will be at the highest point from 13th to 17th and the doctor can test it easily.
3. Maintaining audit trail for regulated environments: an audit trail is like a commit history for a clinical data. For data it answers who did that, when and what changed. Regulated environments mean CFR (code of federal regulations) and HIPAA are govt bodies which make laws regarding patient data and they specify that audit trails should be maintained
4. Deliver analysis-ready datasets which consist of the patient data.

## Core concepts (how the system works)

### Study and protocols
a study is a collection of data related to the patient. A study is a database which contains tables. A study contains:
1. protocol: protocol has data regarding visits and windows. It contains: required visits, timing of visits, what data is collected at each visit (remarks), windows. Eg a protocol will contain:
    a. required visits: it contains the visit name and whether its required or not
    visit name                  required
    baseline (initial visit)    Yes
    Month 1                     Yes
    Month 3                     No
    etc...
    b. Timing of visits: It contains the visit name and the target day (Jan 15th in the eg given in line 17)
    visit name      Target
    Baseline        Day 0
    Month 1         Day 30 (30 days since baseline)
    Month 3         Day 90 (90 days since baseline)
    etc ...
    c. Visit windows: it contains visit name, window before and window after which are represented as -x/+y
    Visit name      WindowBefore        WindowAfter
    Baseline        0                   0 (no windows for baseline as the initial data is imp to be scheduled that day only)
    Month 1         -7                  +14
    etc...
    d. Data collected during each visit: for every visit there can be different data taken from patient. Eg:
    Visit name

    Note that protocol is not a db or a table rather is a set of rules. The protocols like required visits, timing of visits etc. are the tables

2. Participation enrollment: whenever a participant is enrolled we record these details:
    a. Code: this will be a code which uniquely identifies a participant. Eg: ABC-001
    b. Consent: the participant gives consent by filling out these fields: 
    ```yaml
        consent_given: True
        consent_date: 01/01/2026
    ```
    internally there will be a check that if `consent_given` is false then the participant will not be enrolled in our system

3. Data export: the app will export all the tables given above in a csv file.

4. Audit trail: keep a track of changes. The changes to be recorded are:
    a. creating or editing participant details
    b. changing visit details
    c. exporting data

## Project setup
### Install Docker
we'll be using docker where we'll build an image. The advantage of this is that we can easily start/stop the project and also run all the other services we'll be using with a single command.
Before installing docker, install wsl2: in a terminal type `wsl --install`
Installing:
1. go to docker [website](https://www.docker.com/) -> click on `download docker desktop` -> choose `download for windows AMD64`.
2. While installing, check the option `use wsl2 instead of hyper-v` as we're going to use ubuntu with wsl2. Leave other options default and install. After installing, it'll ask to restart.

Note: By default after restarting docker and wsl should be integrated automatically. If it doesn't happen (due to wsl process not starting automatically after restart) then go to docker desktop -> settings (in top) -> resources -> wsl integration. There click on `enable integration ...` option and toggle ubuntu in `enable integration with additional distros` and click on `Apply and restart` button.

To check if docker was integrated with wsl, launch wsl and type `docker --version` and you should see docker's version.

## Project folder setup
here we'll set up the folders which constitute the various parts of our web app.
Open explorer -> go to this project folder -> hold down shift key and right click and click open linux shell here. This opens wsl with pwd as this folder.
Before doing this make sure that the folder name where your project name is without any spaces.
Make 2 folders called apps and config: `mkdir -p apps config`
Inside the folder apps, create the following subfolders: `mkdir -p apps/studies apps/participants apps/forms apps/audit apps/exports`

## Root folder
from hereon root folder will mean where the current project is i.e `longitudinal-edc/` is the project root folder

## Create requirements.txt
`requirements.txt` will contain all the libraries we'll need for this project. In the root folder create that file and add this:
```txt
Django>=5.0,<6.0
djangorestframework>=3.15
psycopg[binary]>=3.1
redis>=5.0
celery>=5.4
python-dotenv>=1.0
```
The `>=` here means the version must be >= to the given version. Additionally for Django you'll see `>=50,<6.0` which means version must be >= 5.0 and must be < 6.0

This is what each packages do:
1. Django: this is the main web framework of our web app. Due to this our app can take requests, show ui, talk with db etc
2. djangorestframework: it is an extension which is used to build rest apis with django
3. psycopg[binary]: psycopg is postgresql db driver which connects django to the postgres db. The `[binary]` gives us the precompiled code. This means that we need not compile the driver code everytime, the driver code is already compiled and it just runs whenever there is a db request. The adv is that it's faster
4. redis: redis provides fast in-memory data storage. We'll use it as a message queue. This is used with celery
5. celery: its used to run tasks asynchronously. This is used when we export datasets
6. python-dotenv: a utility used for loading env variables from `.env` file

## how are celery and redis used
task queues are queues which contain task in them and it is used to distribute the tasks to across different processes. In our project the task queue is redis.

Celery's job is to accept the task from redis and start processing them asynchronously. The process spawned for this is called worker process. The code for the worker process is given in config/celery.py

## Building Dockerfile
Create a file called `Dockerfile` in project root. Explanation given in that file. Also create a `.dockerignore` file.

## Configuring celery
`celery.py` is a configuration file for celery package. It basically contains the code for the worker. Create the file here `config/celery.py` and write the config

Next create an `__init__.py` in config folder. In that first import the celery object from `celery.py` and add that into `__all__` tuple. This is done cuz celery won't just import `celery.py` but imports the whole `config` folder, so we need to expose the celery object by importing it in `__init__.py` and then including it in `__all__`.

Finally in `config/settings.py` add some vars which define the configuration

## Building docker compose
in project root, create a file called `docker-compose.yml`

## Running docker compose
in wsl terminal, go to your project root and run this command: `docker composer run --rm web django-admin startproject config .`. The django-admin command will be run in the web container.
Once you run the above command, the images for postgres and redis will be downloaded. Then the `build-essential` package and packages from `requirements.txt` will be downloaded in the `web` container.

Also you can see that django has been installed in the folder `config`

## Configure django to use postgres from docker
go to `settings.py` in config and scroll to `DATABASES` object and set it to postgres

## Specifying hosts which can connect to backend
in `ALLOWED_HOSTS`, add the values "localhost" and "127.0.0.1" so that we can connect to this backend from our localhost

## Creating apps
our web app will contain multiple webpages which handle a particular functionality. For each of these functionalities we'll create separate django apps. The apps are:
1. studies
2. participants
3. forms
4. audit
5. exports

to create these apps use the command `docker compose run --rm web python manage.py startapp <app-name> apps/<app-name>`.

After doing this add the app names into `INSTALLED_APPS` in `settings.py`. Also in `INSTALLED_APPS` add `rest_framework`, this enables the django rest framework.

We also need to apps `__init__.py` to `apps` folder and the django apps we created. We do this so that we can import them as packages whenever needed. To do that use this command:
`touch apps/__init__.py` and `touch apps/<app1>/__init__.py apps/<app2>/__init__.py` for app1 to app5

## Start all containers
enter the command `docker compose up --build` and then open `http://localhost:8000`

## what each of the apps means
study: it represents a real clinical study. It contains info about the study conducted. Eg: name, description of the study
participants: this contains all the participants (patients) details.
visit: this represents a timepoint. our app supports 3 timepoints: baseline, month 3 and year 1
form: the data collected from a patient during visit
audit: contains the audit trail
exports: contains code related to exporting datasets using celery

# Creating models
now we'll begin with the project. We'll start by creating the models

## Study model
in `apps/studies/models.py` create the model