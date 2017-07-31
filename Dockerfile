# Use an official Python runtime as a parent image
#FROM python:3.6-slim
FROM fedora:26

RUN yum update -y; yum clean all

# Install any needed packages specified in requirements.txt
#RUN yum -y upgrade && yum -y install xorg-x11-server-Xvfb xorg-x11-fonts-Type1 xorg-x11-fonts-75dpi
RUN yum -y install firefox xorg-x11-server-Xvfb xorg-x11-fonts-Type1 xorg-x11-fonts-75dpi

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app


ADD https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz /app
RUN tar xf /app/geckodriver-v0.18.0-linux64.tar.gz -C /usr/local/bin # geckodriver
#ENV PATH="./:${PATH}"

RUN pip3 install -r requirement.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME ahaNewCase

# Run app.py when the container launches
#CMD ["python3", "./ahaNewCase.py --toAddr=wenshi@redhat.com --fromAddr=mail.walker.shi@gmail.com --fromAddrPW=gmailshi1985 --rhuser=rhn-support-wenshi --rhpass=Wasabidou@3"]
#CMD ["python3", "./ahaNewCase.py"]

ENTRYPOINT ["./ahaNewCase.py"]
CMD ["--help"]
