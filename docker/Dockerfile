FROM python:3.9
LABEL maintainer "Nicola Bernini <nicola.bernini@gmail.com>"
COPY requirements.txt .
RUN apt-get update && apt-get -y install sudo

# Create User 
ARG user=mev
ARG password=mev
RUN useradd -m ${user} && echo "${user}:${password}" | chpasswd && adduser mev sudo

# Switch to user 
USER mev

# Install Python Requirements
RUN pip3 install -r requirements.txt


# Initial Dir
WORKDIR /project
