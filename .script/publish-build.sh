#!/bin/sh

version=`grep "version:" galaxy.yml | cut -d ":" -f 2 | cut -d " " -f 2`
#version = 1.0.0
echo $version
echo $TRAVIS_BUILD_NUMBER
datestr=$(date +%Y%m%d%H%M)
echo $datestr
file=ibm-power_ibmi-${version}.tar.gz
dir=projects/a/ansible-for-i/${version}/${datestr}-$TRAVIS_BUILD_NUMBER

IP=bejgsa.ibm.com

lftp -u ${GSA_USER},${GSA_PASSWORD} sftp://${IP} << EOF
mkdir -p ${dir}
cd  ${dir} 
put ${file}
by
EOF
