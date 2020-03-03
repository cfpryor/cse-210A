#!/bin/bash

EXPERIMENTS='collective-classification jester'

# Path variables
BIN='bin/'

TUFFY_DIR='tuffy-0.3-jun2014/'
TUFFY_JAR='tuffy.jar'
TUFFY_ZIP='tuffy-0.4-july2014.zip'
TUFFY_URL='http://i.stanford.edu/hazy/tuffy/download/'${TUFFY_ZIP}

PSL_EXAMPLES='psl-examples'
PSL_URL='https://github.com/linqs/psl-examples.git'

trap exit SIGINT

# Grab Tuffy JAR
function tuffy::load() {
   echo 'Setting up Tuffy...'
   if [ -f "${BIN}${TUFFY_JAR}" ] ; then
      echo 'Jar exists: Skipping Request'
      return
   fi

   echo 'Requesting jar...'
   curl -O ${TUFFY_URL} > /dev/null
   unzip ${TUFFY_ZIP} > /dev/null
   mv ${TUFFY_DIR}${TUFFY_JAR} ${BIN}${TUFFY_JAR} 
   rm -r ${TUFFY_DIR}
   rm ${TUFFY_ZIP}
}

# Clone psl-examples
function psl::load() {
   echo 'Setting up PSL...'
   if [ -d "${PSL_EXAMPLES}" ] ; then
      echo 'PSL exists: Skipping Request'
      return
   fi

   echo 'Requesting repo...'
   git clone ${PSL_URL} > /dev/null
}

# Make the bin directory if it doesn't exist
mkdir -p ${BIN}

psl::load
tuffy::load

for experiment in $EXPERIMENTS; do
   echo ${experiment}
done
