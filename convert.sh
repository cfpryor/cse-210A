#!/bin/bash

readonly BASE_DIR=$(realpath "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )")

readonly TUFFY_EXAMPLES="${BASE_DIR}/tuffy-examples"
readonly PSL_EXAMPLES="${BASE_DIR}/psl-examples"

function main() {
   trap exit SIGINT

   local experiments=$@ 

   for experiment in ${experiments}; do
      echo "INFO: Converting data for ${experiment}"
      getData::tuffy ${TUFFY_EXAMPLES} ${PSL_EXAMPLES} ${experiment}
   done
}

function getData::tuffy() {
   local tuffypath=$1
   local pslpath=$2
   local experiment=$3

   pushd . > /dev/null

   cd ${BASE_DIR}/scripts
   python3 prepare-tuffy.py ${tuffypath} ${pslpath} ${experiment}

   popd > /dev/null
}

main "$@"
