#!/bin/bash

# Start Web Server
echo "Web Start"
/usr/sbin/nginx &

# Start server
echo "Starting server"
/usr/sbin/sshd -D -o ListenAddress=0.0.0.0
