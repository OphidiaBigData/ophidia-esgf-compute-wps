#!/bin/bash

cd ${1}/${2}
if [ $? -ne 0 ]; then
	exit 1
fi

ncrcat ${1}/${2}/*.nc ${1}/${2}.nc
if [ $? -ne 0 ]; then
	exit 2
fi

cd ${1}
if [ $? -ne 0 ]; then
	exit 3
fi

rm -rf ${1}/${2}

exit 0

