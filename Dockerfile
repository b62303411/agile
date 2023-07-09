FROM python:3.9

# set up working directory
RUN mkdir /app
WORKDIR /app

# copy requirements and install them
COPY requirements.txt /app
RUN pip install -r requirements.txt

# copy source
COPY . /app

# expose port for application
EXPOSE 80

# command to run app when container is started
CMD ["python","manage.py","runserver"]