#!/bin/bash
function jj(){
    RESULT_FILE=/tmp/_jj_result
    jj-menu --result-file=${RESULT_FILE}
    if [ $? = 0 ]; then
        history -s `cat ${RESULT_FILE}` 2>/dev/null
        source ${RESULT_FILE}
    fi
}
