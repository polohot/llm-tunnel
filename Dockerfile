# THIS STEP WILL DOWNLOAD PYTHON
# CHECK YOUR PYTHON VERSION, CURRENT IS 3.12.4, SO ONLY PUT 3.12
FROM python:3.12-slim
# UPDATE AS USUAL
RUN apt-get update
# CREATE DIRECTORY
RUN mkdir /app
# SET THIS DIRECTORY AS WORKING DIRECTORY
WORKDIR /app
### INSTALL DEPENDENCY
### To create requirements.txt use this command in cmd consol : pip3 freeze > requirements.txt
# COPY FROM ROOT TO APP FOLDER
COPY requirements.txt /app/
# GOOD PRACTICE TO UPGRADE PIP FIRST
RUN pip install --upgrade pip
# NOW RUN INSTALL PACKAGES
RUN pip install --no-cache-dir --upgrade -r requirements.txt
### COPY ALL FILES FROM ROOT TO DOCKER FOLDER
# . MEANING START FROM THE WORKING DIRECTORY
# / MEANING START FROM ROOT
COPY . /app
### NOT REQUIRED, UNLESS WANT TO SPECIFY PORT
EXPOSE 8080
### START SERVER
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port","8080"]