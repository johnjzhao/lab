#!/bin/bash

# NOTE: Must be run inside context of rules engine container.
# Packaged as standalone script due to jenkinsfile/groovy syntax issues when executed natively in pipeline.

cd /app/RulesEngine/ && ls
export WORKSPACE=$PWD
find . -name "*.log" -exec rm -rf {} \\;
PROPERTY_FILE=$WORKSPACE/Rules_Engine.properties
touch $PROPERTY_FILE
export PYTHONUSERBASE=$WORKSPACE
UN_RE_DIR=/app/lib/python3.6/site-packages/un_re
export PYTHONPATH=$UN_RE_DIR/Antlr:$PYTHONPATH
export PYTHONPATH=$UN_RE_DIR:$PYTHONPATH
XML_LIST=$WORKSPACE/xml_files.lst
find $WORKSPACE/Teradata/src -name 'update.xml' | grep -v do_not_use | sort > $XML_LIST

INI_FILE=/app/RulesEngine/PyDream.ini
NUM_FAILED=0

XML_DIR=$WORKSPACE/Teradata/src/
XML_FILE=$WORKSPACE/Teradata/src/update.xml

LOG_FILE=$WORKSPACE/Rules_Engine.log
env | sort
python3.6 -B /app/bin/UN_RE -i /app/PyDream.ini -v | tee Rules_Engine.log

cat $WORKSPACE/Teradata/src/update.xml
cat $WORKSPACE/Teradata/src/update.xml.nocom
