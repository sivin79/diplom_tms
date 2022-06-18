FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN mkdir my_flask_app
ADD app/ /my_flask_app
WORKDIR /my_flask_app
RUN ls -l
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD [ "python3", "app.py"]


