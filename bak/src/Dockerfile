FROM python:3.6
MAINTAINER XenonStack

# Creating Application Source Code Directory
RUN mkdir -p /dataprocess/src

# Setting Home Directory for containers
WORKDIR /dataprocess/src

WORKDIR /tmp
# Installing python dependencies
COPY requirements.txt /dataprocess/src
COPY TDengine-client-2.4.0.4-Linux-x64.tar.gz /tmp

# Copying src code to Container
COPY . /dataprocess/src
# Application Environment variables
ENV APP_ENV development
RUN cd  /tmp
RUN  tar -xzf /tmp/TDengine-client-2.4.0.4-Linux-x64.tar.gz   
RUN cd  /tmp/TDengine-client-2.4.0.4 \
&& ./install_client.sh
RUN pip install --no-cache-dir -r /dataprocess/src/requirements.txt

# Exposing Ports
EXPOSE 5035

# Setting Persistent data
VOLUME ["/app-data"]


#CMD /dataprocess/src/init_commands.sh & sleep infinity 

WORKDIR /dataprocess/src
# Running Python Application
CMD cd /dataprocess/src\
&& ./sleep-app.sh& sleep infinity 

#CMD ["python", "di.py"]
#CMD ["python", "DataProcess.py"]