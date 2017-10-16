#!/bin/bash

LOG_FILE=./logs/`date +%Y-%m-%d_%H:%M.log`

function log {
    echo $1 | tee -a ${LOG_FILE}
}

log "About to kill <<home monitoring>>"
kill $(ps aux | grep -v "grep" | grep "run.py" | awk '{print $2}') | tee -a ${LOG_FILE} 2>&1

log "About to run <<home monitoring>>"
./run.sh &

 