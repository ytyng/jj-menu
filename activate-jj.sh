#!/bin/bash
function jj(){
    RESULT_FILE=/tmp/_jj_result
    jj-menu --result-file=${RESULT_FILE}
    if [ $? == 0 ]; then
        source ${RESULT_FILE}
        history -s `cat ${RESULT_FILE}`
    fi
}
