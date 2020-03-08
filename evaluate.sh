#!/bin/bash

readonly BASE_DIR=$(realpath "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )")

readonly TUFFY_EXAMPLES="${BASE_DIR}/tuffy-examples"
readonly PSL_EXAMPLES="${BASE_DIR}/psl-examples"

function main() {
   trap exit SIGINT

   local experiment=$1 
   local evaluation=$2 

   evaluate ${experiment} ${evaluation}
}

function evaluate() {
   local experiment=$1
   local evaluation=$2

   pushd . > /dev/null

   cd ${BASE_DIR}/scripts
   python3 evaluate.py ${experiment} ${evaluation} ${PSL_EXAMPLES} ${TUFFY_EXAMPLES}

   popd > /dev/null
}

main "$@"
