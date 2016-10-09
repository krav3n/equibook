FROM baseimage

# Global python dependencies & mysql-client
RUN apt-get install -y --force-yes python-pip python-dev python-setuptools gcc libmysqlclient-dev mysql-client

# Install latest version of fabric and pip
RUN easy_install -U Fabric==1.10.0 pip==6.0.6


############
# Add python requirements files and install all packages in them

RUN apt-get install -y swig libssl-dev

ADD requirements/ /
RUN pip install -r /dev.txt


# ###########
# # Default start script

CMD ["/sbin/my_init"]
