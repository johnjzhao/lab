#!/bin/bash

Cit="War"

parStr="cat ./test-input-01.txt "

Cit1=`$parStr |awk -F'.' '{print NR, ",", "." $2}' |awk -F',' '{print $4, ",", $3, ",", $2, ","  $1}' |sort |grep -F -e $Cit |awk -F',' '{print $4, ",", $2, NR, $3}'|sed 's/  //g'|sed 's/ //g'|sed 's/Warsaw/Warsaw0/g' |sed 's/Warsaw010/Warsaw10/g'>/tmp/tmp.1`
Cit="Par"
Cit2=`$parStr |awk -F'.' '{print NR, ",", "." $2}' |awk -F',' '{print $4, ",", $3, ",", $2, ","  $1}' |sort |grep -F -e $Cit |awk -F',' '{print $4, ",", $2, NR, $3}'|sed 's/  //g'|sed 's/ //g'|sed 's/Warsaw/Warsaw0/g' |sed 's/Warsaw010/Warsaw10/g'>>/tmp/tmp.1`

Cit="Lon"
Cit3=`$parStr |awk -F'.' '{print NR, ",", "." $2}' |awk -F',' '{print $4, ",", $3, ",", $2, ","  $1}' |sort |grep -F -e $Cit |awk -F',' '{print $4, ",", $2, NR, $3}'|sed 's/  //g'|sed 's/ //g'|sed 's/Warsaw/Warsaw0/g' |sed 's/Warsaw010/Warsaw10/g'>>/tmp/tmp.1`

sortStr="cat /tmp/tmp.1"
$sortStr |sort -t, -nk1 |awk -F',' '{print $2}'

rm -f /tmp/tmp.1
