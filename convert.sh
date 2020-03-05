#!/bin/bash

# Path variables
SCRIPTS='scripts/'

TUFFY_EXAMPLES='tuffy-examples/'
TUFFY_PREPARE='prepare-tuffy.py'

PSL_EXAMPLES='psl-examples/'

function main() {
  experiments=$@ 

  for experiment in ${experiments}; do
      echo 'INFO: Converting data for '${experiment}
      getData::tuffy ${TUFFY_EXAMPLES} ${PSL_EXAMPLES} ${experiment}
   done
}

function getData::tuffy() {
   tuffypath=$1
   pslpath=$2
   experiment=$3

   pushd . > /dev/null

   cd "${SCRIPTS}"
   python3 "${TUFFY_PREPARE}" '../'${tuffypath} '../'${pslpath} ${experiment}

   popd > /dev/null
}

main "$@"
