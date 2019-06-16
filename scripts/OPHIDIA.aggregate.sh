#!/bin/bash

cd ${2}
ncrcat ${1} ${2}/${3}.nc
if [ $? -ne 0 ]; then
	exit 1
fi

exit 0

