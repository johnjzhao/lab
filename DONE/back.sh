#!/bin/bash

SOURCE="/tmp/sysctl.tar.gz /etc/sysctl.conf /etc/sysctl.d/"
TARGET="/tmp/sysctl-$(date +%F-%H-M).tar.gz

if [ ! -z "$1" ]; then
	SOURCE=$1
else
	echo "Nosource provided."
	echo "Using default: $SOURCE"
fi

TARGET_DIR=$(direname $TARGET)

if [ ! -d "$TARGET_DIR" ]; then
	echo "Target folder is not exist or not a directory!"
	exit 2
fi

tar -zcv ${TARGET} ${SOURCE} 1> /dev/null 2> /dev/null

if [ $? -eq 0 ]; then
	echo "Backup successful."
else
	echo "Backup failed."
fi
