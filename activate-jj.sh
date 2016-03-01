#!/bin/bash
function jj(){
    RESULT_FILE=/tmp/_jj_result
    jj-menu --result-file=${RESULT_FILE}
    if [ $? == 0 ]; then
        history -s `cat ${RESULT_FILE}`
        source ${RESULT_FILE}
    fi
}
