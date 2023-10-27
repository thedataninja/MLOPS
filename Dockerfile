FROM --platform=linux/amd64 ubuntu:20.04
MAINTAINER "Ashish Lakhani"

RUN apt-get update -qq
RUN apt-get install supervisor -qq
RUN apt-get install wget -qq
RUN apt-get install python3-pip -qq


EXPOSE 5000/tcp
EXPOSE 8501/tcp
ENV CURLOPT_SSL_VERIFYHOST=0
ENV CURLOPT_SSL_VERIFYPEER=0
ENV SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True

RUN wget 'http://storage.googleapis.com/tensorflow-serving-apt/pool/tensorflow-model-server-universal-2.8.0/t/tensorflow-model-server-universal/tensorflow-model-server-universal_2.8.0_all.deb'
RUN dpkg -i tensorflow-model-server-universal_2.8.0_all.deb


ENV APP_DIR /app
RUN mkdir -p $APP_DIR/intent-entity-api/intent_entity_detection

COPY intent-entity-detection/__init__.py intent-entity-detection/views.py $APP_DIR/intent-entity-api/intent_entity_detection/

COPY run.py exceptions.py $APP_DIR/intent-entity-api/
COPY models/ /models/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt

WORKDIR $APP_DIR/intent-entity-api/

# for local development
#ENTRYPOINT ["python3", "-u", "run.py"]

ENTRYPOINT ["/usr/bin/supervisord"]
