FROM ubuntu AS app

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:longsleep/golang-backports
RUN apt-get install -y golang-go gdb make

# Set the working directory
WORKDIR /app
COPY src/server/server /app/server

# Install any other required dependencies here

# Expose the port for the server
EXPOSE 8890

# Start the shell for interactive debugging
#CMD ["/bin/bash"]
ENV CTF_FLAG="BarSides{dr!p_dr0p_dr!p_dr0p}"
ENV CTF_PORT=8890
ENV CTF_DATE="20241003"
ENTRYPOINT ["/app/server"]

# docker build -t rev-intermediate
# docker run -it --rm -p 8888:8888 -v "${PWD}:/app" rev-intermediate

# use the jail base image