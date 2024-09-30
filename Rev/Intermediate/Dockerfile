FROM ubuntu AS app

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:longsleep/golang-backports
RUN apt-get install -y golang-go gdb make

# Set the working directory
WORKDIR /app

# Install any other required dependencies here

# Expose the port for the server
EXPOSE 8080

# Start the shell for interactive debugging
CMD ["/bin/bash"]

# docker build -t rev-intermediate
# docker run -it --rm -p 8888:8888 -v "${PWD}:/app" rev-intermediate

# use the jail base image