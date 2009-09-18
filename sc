#!/bin/bash

count() {
	echo $(find "$1" -mindepth 1 | wc -l) items
}

printCount() {
	if [ -d "$1" ]; then
		echo -n $'\t'
		count "$1"
	fi
}

declare -i code=0

if [ $# -eq 0 ]; then
	du -sh . | awk '{print $1}'
	[ ${PIPESTATUS[0]} -eq 0 ] && count .
	code+=$?
else
	du -s "$@" | sort -nr | awk '{
		sub($1, "");
		sub(/^[[:blank:]]+/, "");
		print;
	}' | while read; do
		du -sh "$REPLY" && printCount "$REPLY"
		code+=$?
	done
	code+=${PIPESTATUS[0]}
fi

exit $code
