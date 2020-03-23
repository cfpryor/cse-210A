#!/bin/bash

readonly BASE_DIR=$(realpath "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )")

readonly PSL_EXAMPLES="${BASE_DIR}/psl-examples"
readonly TUFFY_EXAMPLES="${BASE_DIR}/tuffy-examples"

function main() {
   trap exit SIGINT 

   experiments=$@ 

   # Does not handle weight learning
   for experiment in ${experiments}; do
      for split in "${PSL_EXAMPLES}/${experiment}/data/${experiment}/"*; do
         echo "INFO: Running PSL for ${experiment} split ${split}"
         run::psl ${experiment} $(basename ${split})

         echo "INFO: Running Tuffy for ${experiment} split ${split}"
         run::tuffy ${experiment} $(basename ${split})
      done
   done
}

function run::psl(){
   local experiment=$1
   local split=$2

   local split_dir="${PSL_EXAMPLES}/${experiment}/data/${experiment}/${split}"
   local log="${split_dir}/eval/out.txt"
   local err="${split_dir}/eval/out.err"

   local cli_dir="${PSL_EXAMPLES}/${experiment}/cli"
   local tmp_dir="${PSL_EXAMPLES}/${experiment}/data/${experiment}/tmp"

   if [ -d ${tmp_dir} ] ; then
      rm -r ${tmp_dir}
   fi

   cp -r ${split_dir} ${tmp_dir}

   pushd . > /dev/null

   cd ${cli_dir}
   /usr/bin/time -v ./run.sh > ${log} 2> ${err}
   mv inferred-predicates ${split_dir}/eval

   popd > /dev/null
}

function run::tuffy(){
   local experiment=$1
   local split=$2

   local split_dir="${TUFFY_EXAMPLES}/${experiment}/data/${experiment}/${split}"
   local log="${split_dir}/eval/out.txt"
   local err="${split_dir}/eval/out.err"

   local prog="${TUFFY_EXAMPLES}/${experiment}/prog.mln"
   local query="${TUFFY_EXAMPLES}/${experiment}/query.db"
   local evidence="${split_dir}/eval/evidence.db"
   local results="${split_dir}/eval/results.txt"

   if [ -f "${split_dir}/eval/query.db" ] ; then
      query="${split_dir}/eval/query.db"
   fi

   # Runs with marginal
   pushd . > /dev/null

   cd ${BASE_DIR}/scripts
   /usr/bin/time -v java -Xmx40G -Xms40G -jar tuffy.jar -i ${prog} -e ${evidence} -queryFile ${query} -r ${results} -marginal > ${log} 2> ${err}

   popd > /dev/null
  
}

main "$@"
