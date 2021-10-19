FROM python:3.7.2-stretch
MAINTAINER GeoKapti "info@geokapti.nl"

WORKDIR /app
ADD . /app

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "run.py"]
# in case we wish an apache/ngix infront
# we could use use uWSGI
#CMD ["uwsgi", "app.ini"]




