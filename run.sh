#!/bin/bash

readonly BASE_DIR=$(realpath "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )")
readonly PSL_EXAMPLES="${BASE_DIR}/psl-examples"

BIN='bin/'
DATA='data/'
EVAL='eval/'

# Tuffy path and filenames
TUFFY_EXAMPLES='tuffy-examples/'
TUFFY_EVID='evidence.db'
TUFFY_PRED='predicates.txt'
TUFFY_PROG='prog.mln'
TUFFY_QUERY='query.db'
TUFFY_RESULTS='results.txt'
TUFFY_LOG='log.txt'

function main() {
   experiments=$@ 

   # Does not handle weight learning
   for experiment in ${experiments}; do
      for split in ${TUFFY_EXAMPLES}${experiment}'/'${DATA}${experiment}'/'*'/'; do
         t_prog='../'${TUFFY_EXAMPLES}${experiment}'/'${TUFFY_PROG}
         t_evidence='../'${split}${EVAL}${TUFFY_EVID}
         t_query='../'${TUFFY_EXAMPLES}${experiment}'/'${TUFFY_QUERY}
         t_results='../'${split}${EVAL}${TUFFY_RESULTS}
         t_log='../'${split}${EVAL}${TUFFY_LOG}

         echo 'INFO: Running Tuffy for '${experiment}' split '${split}
         #run::tuffy ${t_prog} ${t_evidence} ${t_query} ${t_results} ${t_log}
         echo 'INFO: Running PSL for '${experiment}' split '${split}
         run::psl ${experiment} $(basename ${split})
      done
   done
}

function run::psl(){
   local cli_dir=${PSL_EXAMPLES}'/'$1'/cli'
   local split_dir=${PSL_EXAMPLES}'/'$1'/data/'$1'/'$2
   local tmp_dir=${PSL_EXAMPLES}'/'$1'/data/'$1'/tmp'
   local log=${split_dir}'/out.txt'
   local err=${split_dir}'/out.err'

   if [ -d ${tmp_dir} ] ; then
      rm -r ${tmp_dir}
   fi

   cp -r ${split_dir} ${tmp_dir}

   pushd . > /dev/null

   cd "${cli_dir}"
   time ./run.sh > ${log} 2> ${err}
   mv 'inferred-predicates' ${split_dir}

   popd > /dev/null
}

function run::tuffy(){
   prog=$1
   evidence=$2
   query=$3
   results=$4
   log=$5

   # Runs with marginal
   pushd . > /dev/null

   cd "${BIN}"
   /usr/bin/time -v java -Xmx40G -Xms40G -jar tuffy.jar -i ${prog} -e ${evidence} -queryFile ${query} -r ${results} -marginal > ${log}

   popd > /dev/null
  
}

main "$@"
