#!/usr/bin/env bash

# start python with som init code

while true; do
	echo "edsh debug shell, use CTRL-D to reload, CTRL-C to exit"
	python -c '\
		from edsh import *;\
		start()'
	if [[ "$?" == "127" ]]; then
		break
	fi
done
