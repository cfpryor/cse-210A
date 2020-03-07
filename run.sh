#!/bin/bash

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
         run::tuffy ${t_prog} ${t_evidence} ${t_query} ${t_results} ${t_log}
         echo 'INFO: Running PSL for '${experiment}' split '${split}
      done 
   done
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
   /usr/bin/time -v java -jar tuffy.jar -i ${prog} -e ${evidence} -queryFile ${query} -r ${results} -marginal > ${log}

   popd > /dev/null
  
}

main "$@"
