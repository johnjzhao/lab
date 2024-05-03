#!/bin/sh

# NOTE: file pathing assumes execution from project/repo root

### START ###
echo "build-liquibase-dir.sh START"

### Check inputs ###

while getopts ":d:" opt; do
  case $opt in
    d)
        ddl_dir="$OPTARG"
        ;;
    \?)
        echo "Invalid option: -$OPTARG" 1>&2
        echo "Valid options:"
        echo "  -d: ddl directory"
        exit 1
        ;;
    :)
        echo "Invalid argument: Option -$OPTARG missing argument" 1>&2
        exit 1
        ;;
    *)
  esac
done

if [ -z $ddl_dir ];
then
  ddl_dir='ddl'
fi

if [ ! -d "${ddl_dir}" ];
then
    echo "ddl directory '${ddl_dir}' does not exist in ${PWD}"
    exit 1
fi

### Copy changelog ###

echo "Copying changelog files"
mkdir -p liquibase/changelog/
rm -rf liquibase/changelog/*
cp -R "${ddl_dir}/." liquibase/changelog/

ls liquibase/changelog

### COMPLETE ###
echo "build-liquibase-dir.sh DONE"
