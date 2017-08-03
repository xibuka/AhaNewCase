# Use an official Python runtime as a parent image
FROM fedora:26

RUN yum update -y; yum clean all

# Install any needed packages specified in requirements.txt
RUN yum -y install firefox xorg-x11-server-Xvfb xorg-x11-fonts-Type1 xorg-x11-fonts-75dpi

# Set the timezone to Asia/Tokyo
RUN timedatectl set-timezone Asia/Tokyo

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Copy and untar webdriver for firefox
ADD https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz /app
RUN tar xf /app/geckodriver-v0.18.0-linux64.tar.gz -C /usr/local/bin # geckodriver

# Install requirements for python
RUN pip3 install -r requirement.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME ahaNewCase

# Run app.py when the container launches
ENTRYPOINT ["./ahaNewCase.py"]
CMD ["--help"]
