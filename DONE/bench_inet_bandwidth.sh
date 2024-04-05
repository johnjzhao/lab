#!/bin/bash
LOGFILE=bench_inet_bandwidth.log
ISP=StarLink

# tidy up
rm -rf testfile

echo "=== $ISP inet benchmark (downloading 100MByte of random data) started on: $(date '+%Y-%m-%d-%H:%M:%S') ===" >> $LOGFILE;
curl -o testfile https://dwaves.de/testfile 2>&1 | tee -a ${LOGFILE}; 

# output results
cat $LOGFILE;

