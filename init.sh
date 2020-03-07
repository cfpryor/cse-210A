#!/bin/bash

readonly BASE_DIR=$(realpath "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )")

# PSL settings
readonly PSL_VERSION='2.2.1'
readonly POSTGRES_DB='psl'
readonly BASE_PSL_OPTION="--postgres ${POSTGRES_DB} -D log4j.threshold=TRACE -D persistedatommanager.throwaccessexception=false"
readonly AVAILABLE_MEM_KB=$(cat /proc/meminfo | grep 'MemTotal' | sed 's/^[^0-9]\+\([0-9]\+\)[^0-9]\+$/\1/')
readonly JAVA_MEM_GB=$((${AVAILABLE_MEM_KB} / 1024 / 1024 / 5 * 5 - 5))

# Tuffy path variables
readonly TUFFY_EXAMPLES="${BASE_DIR}/tuffy-examples"
readonly TUFFY_URL="http://i.stanford.edu/hazy/tuffy/download/tuffy-0.4-july2014.zip"
readonly TUFFY_BIN="${BASE_DIR}/tuffy-0.3-jun2014"
readonly TUFFY_ZIP="${BASE_DIR}/tuffy-0.4-july2014.zip"

# PSL path variables
readonly PSL_EXAMPLES="${BASE_DIR}/psl-examples"
readonly PSL_URL="https://github.com/linqs/psl-examples.git"
readonly PSL_FETCH_SCRIPT="data/fetchData.sh"

function main() {
   trap exit SIGINT

   local experiments=$@

   psl::load
   tuffy::load

   for experiment in ${experiments}; do
      echo "INFO: Working on setting up ${experiment}"
      getData::psl "${PSL_EXAMPLES}/${experiment}"
      prepare::psl "${PSL_EXAMPLES}/${experiment}"
      getData::tuffy "${TUFFY_EXAMPLES}/${experiment}"
   done
}

function psl::load() {
   echo "INFO: Fetching PSL..."
   if [ -d "${PSL_EXAMPLES}" ] ; then
      echo "PSL exists, skipping request"
      return
   fi

   git clone ${PSL_URL} > /dev/null
}


function tuffy::load() {
   echo "INFO: Fetching Tuffy..."
   if [ -f "${BASE_DIR}/scripts/tuffy.jar" ] ; then
      echo "Jar exists, skipping request"
      return
   fi

   curl -O ${TUFFY_URL}
   unzip ${TUFFY_ZIP}
   mv ${TUFFY_BIN}/tuffy.jar ${BASE_DIR}/scripts/tuffy.jar 
   rm -r ${TUFFY_BIN}
   rm ${TUFFY_ZIP}

   mkdir -p ${TUFFY_EXAMPLES}
}

function getData::psl() {
   local experiment=$1
   local datapath="${experiment}/${PSL_FETCH_SCRIPT}"

   if [ ! -f "${datapath}" ] ; then
      echo "No fetch script, skipping request"
      return
   fi

   pushd . > /dev/null

   cd "$(dirname ${datapath})"
   bash "$(basename ${datapath})"

   popd > /dev/null
}

function prepare::psl() {
   local exampleDir=$1
   local baseName=`basename ${exampleDir}`
   local options=''

   pushd . > /dev/null
      cd "${exampleDir}/cli"

      # Always create a -leared version of the model in case this example has weight learning.
      cp "${baseName}.psl" "${baseName}-learned.psl"

      # Increase memory allocation.
      sed -i "s/java -jar/java -Xmx${JAVA_MEM_GB}G -Xms${JAVA_MEM_GB}G -jar/" run.sh

      # Set the PSL version.
      sed -i "s/^readonly PSL_VERSION='.*'$/readonly PSL_VERSION='${PSL_VERSION}'/" run.sh

      # Disable weight learning.
      sed -i 's/^\(\s\+\)runWeightLearning/\1# runWeightLearning/' run.sh

      # Add in the additional options.
      sed -i "s/^readonly ADDITIONAL_PSL_OPTIONS='.*'$/readonly ADDITIONAL_PSL_OPTIONS='${BASE_PSL_OPTION} ${options}'/" run.sh

      # Disable evaluation, we are only looking for objective values.
      sed -i "s/^readonly ADDITIONAL_EVAL_OPTIONS='.*'$/readonly ADDITIONAL_EVAL_OPTIONS='--infer'/" run.sh

      # Change data directory to temporary data directory.
      sed -i "s/..\/data\/${baseName}\/0\//..\/data\/${baseName}\/tmp\//" ${baseName}-learn.data
      sed -i "s/..\/data\/${baseName}\/0\//..\/data\/${baseName}\/tmp\//" ${baseName}-eval.data

   popd > /dev/null
}

function getData::tuffy() {
   local path=$1
   local experiment=$(basename ${path})
   mkdir -p ${path}
   mkdir -p ${path}/data

   if [ ! -f "${path}/predicates.txt" ] ; then
      touch ${path}/predicates.txt
   fi

   if [ ! -f "${path}/prog.mln" ] ; then
      touch ${path}/prog.mln
   fi

   if [ ! -f "${path}/query.db" ] ; then
      touch ${path}/query.db
   fi

   if [ -d "${BASE_DIR}/scripts/tuffy/${experiment}" ] ; then
      cp ${BASE_DIR}/scripts/tuffy/${experiment}/* ${path}
   fi
}


main "$@"
