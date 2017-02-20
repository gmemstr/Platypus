#!/bin/bash
if [ ! -f .installed ]; then
    echo "First run of script, installing requirements"
    pip install psutils
    touch .installed
fi

screen -dm python Stats.py
echo "Stats.py running @ 127.0.0.1:9000"