from mysql:latest

WORKDIR /flask_app
ADD . /flask_app

USER root
