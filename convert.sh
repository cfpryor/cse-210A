#!/bin/bash

# Path variables
SCRIPTS='scripts/'

TUFFY_EXAMPLES='tuffy-examples/'
TUFFY_PREPARE='prepare-tuffy.py'

PSL_EXAMPLES='psl-examples/'

function main() {
   for experiment in ${experiments}; do
      echo 'INFO: Converting data for '${experiment}
      getData::tuffy ${TUFFY_EXAMPLES}${experiment}'/' ${PSL_EXAMPLES}${experiment}'/'
   done
}

function getData::tuffy() {
   tuffyexamplepath=$1
   pslexamplepath=$2

   pushd . > /dev/null

   cd "${SCRIPTS}"
   python3 "${TUFFY_PREPARE}" ${tuffyexamplepath} ${pslexamplepath}

   popd > /dev/null
}

main "$@"
