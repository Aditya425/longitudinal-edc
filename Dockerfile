# we start with a ubuntu distro (cuz we're running this project in a ubuntu env) with python v3.12 installed. The "-slim" means that the ubuntu will only contain python v3.12 and its related packages and nothing else. We reduce size by installing this instead of a full ubuntu image with everything installed
FROM python:3.12-slim

# this option is related to python. When we run any python file it creates a python byte code file (.pyc) which is the compiled version of our code. This is same as .class files in java. The .pyc file don't serve any use to us and clutters disk space. Hence we add this value to ubuntu's env. The env values are stored as metadata in docker image. While writing python code we'll import these as env values
ENV PYTHONDONTWRITEBYTECODE=1
# this env value will flush all the logs from stdout and stderr of python to the docker's logs.
ENV PYTHONUNBUFFERED=1

# treat /app in the container as the current working directory. This means whenever we login to the container, the pwd will be /app
WORKDIR /app

# runs the following commands in the container
# apt-get install -y --no-install-recommends build-essential: install the build-essential package which gives us a C compiler which is required to run the binaries of psycopg. 
# Some packages have two types of files, essential (which installs the bare minimum to run the package) and recommended (which installs all the required files which contain extra features but takes more space). The '--no-install-recommends' flag installs only the essential files of the given package
# The cache or temp files related to installation are stored in /var/lib/apt/lists/ we're deleting them to save space
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# copying requirements.txt file to /app in container
COPY requirements.txt /app/

# install everything present in the requirements.txt file. The "--no-cache-dir" removes the downloaded packages after installing. Its same as deleting "setup.exe" after installing the program
RUN pip install --no-cache-dir -r requirements.txt

# copies everything present in project root (in local machine) to docker container's /app folder
COPY . /app/