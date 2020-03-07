#!/bin/bash

# Path variables
BIN='bin/'
DATA='data/'
SCRIPTS='scripts/'

TUFFY_BIN='tuffy-0.3-jun2014/'
TUFFY_JAR='tuffy.jar'
TUFFY_ZIP='tuffy-0.4-july2014.zip'
TUFFY_URL='http://i.stanford.edu/hazy/tuffy/download/'${TUFFY_ZIP}
TUFFY_EXAMPLES='tuffy-examples/'
TUFFY_PREPARE='prepare-tuffy.py'
TUFFY_PREDICATES='predicates.txt'
TUFFY_MODEL='prog.mln'
TUFFY_QUERY='query.db'
TUFFY_CONF='tuffy.conf'

PSL_EXAMPLES='psl-examples/'
PSL_URL='https://github.com/linqs/psl-examples.git'
PSL_FETCH_SCRIPT=${DATA}'fetchData.sh'

function main() {
   trap exit SIGINT

   experiments=$@

   # Make the bin directory if it doesn't exist
   mkdir -p ${BIN}

   psl::load
   tuffy::load

   for experiment in ${experiments}; do
      echo 'INFO: Working on setting up '${experiment}
      getData::psl ${PSL_EXAMPLES}${experiment}'/'${PSL_FETCH_SCRIPT} 
      getData::tuffy ${TUFFY_EXAMPLES}${experiment}'/' ${PSL_EXAMPLES}${experiment}'/'
   done
}

# Clone psl-examples
function psl::load() {
   echo 'INFO: Fetching PSL...'
   if [ -d "${PSL_EXAMPLES}" ] ; then
      echo 'PSL exists, skipping request'
      return
   fi

   echo 'Requesting repo...'
   git clone ${PSL_URL} > /dev/null
}


# Grab Tuffy JAR
function tuffy::load() {
   echo 'INFO: Fetching Tuffy...'
   if [ -f "${BIN}${TUFFY_JAR}" ] ; then
      echo 'Jar exists, skipping request'
      return
   fi

   echo 'Requesting jar...'
   curl -O ${TUFFY_URL} > /dev/null
   unzip ${TUFFY_ZIP} > /dev/null
   mv ${TUFFY_BIN}${TUFFY_JAR} ${BIN}${TUFFY_JAR} 
   rm -r ${TUFFY_BIN}
   rm ${TUFFY_ZIP}
   cp ${SCRIPTS}${TUFFY_CONF} ${BIN}

   mkdir -p ${TUFFY_EXAMPLES}
}

function getData::psl() {
   datapath=$1

   if [ ! -f "${datapath}" ] ; then
      echo 'No fetch script, skipping request'
      return
   fi

   pushd . > /dev/null

   cd "$(dirname ${datapath})"
   bash "$(basename ${datapath})"

   popd > /dev/null
}

function getData::tuffy() {
   tuffyexamplepath=$1
   pslexamplepath=$2
   mkdir -p ${tuffyexamplepath}
   mkdir -p ${tuffyexamplepath}${DATA}

   if [ ! -f "${tuffyexamplepath}${TUFFY_PREDICATES}" ] ; then
      touch ${tuffyexamplepath}${TUFFY_PREDICATES}
   fi

   if [ ! -f "${tuffyexamplepath}${TUFFY_MODEL}" ] ; then
      touch ${tuffyexamplepath}${TUFFY_MODEL}
   fi

   if [ ! -f "${tuffyexamplepath}${TUFFY_QUERY}" ] ; then
      touch ${tuffyexamplepath}${TUFFY_QUERY}
   fi
}

main "$@"
