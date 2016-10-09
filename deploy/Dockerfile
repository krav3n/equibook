# base docker image
FROM base

############
# RabbitMQ

# Install erlang dependency and rabbitmq-server
RUN apt-get install -qqy --force-yes esl-erlang rabbitmq-server


#########
# MySQL

# MySQL Installation (Required to be runned before installing mysql-server)
RUN echo "mysql-server mysql-server/root_password password abcd" | debconf-set-selections && \
    echo "mysql-server mysql-server/root_password_again password abcd" | debconf-set-selections

# Install mysql server 5.5
RUN apt-get install -qqy mysql-server

# Create all required folders used by this image
RUN mkdir -p /var/lib/mysql/  && \
    mkdir -p /etc/service/mysql && \
    mkdir -p /etc/service/celery && \
    mkdir -p /etc/service/rabbitmq

# Add serverconf and setup.sh
ADD mysql/my.cnf /etc/mysql/my.cnf
ADD mysql/setup.sh /etc/mysql/setup.sh

# Add all run service scripts
ADD mysql/runit-service-files/ /etc/service
ADD rabbitmq/runit-service-files /etc/service

# Change permissions for files that require it
RUN chmod +x /etc/service/mysql/run \
             /etc/service/celery/run \
             /etc/service/rabbitmq/run \
             /etc/mysql/setup.sh && \
    chmod -R 755 /var/lib/mysql && \
    chmod 0644 /etc/mysql/my.cnf

# Install database and add users and set permissions
RUN "/etc/mysql/setup.sh"


##########
# Python

# Global python dependencies
RUN apt-get install -qqy --force-yes libmysqlclient-dev libxml2-dev libxslt-dev libjpeg-dev

# Install Fabric and upgrade pip to the latest version and then install all python packages
# Requirements file is added in base image
RUN /usr/local/bin/pip install -r /opt/dev.txt

# Remove PIL and replace with PILLOW for python 2.7 compability
RUN /usr/local/bin/pip uninstall -y pil && /usr/local/bin/pip install pillow==2.5.1

# Default image entrypoint
CMD ["/sbin/my_init"]
