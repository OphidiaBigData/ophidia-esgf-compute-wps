#!/bin/bash

# Input parameters
# 1: output path
# 2: output filename
# 3: list of input file
# 4: input variable

BASE_PATH=${OPH_SCRIPT_DATA_PATH}/${1}

mkdir -p ${BASE_PATH}/${2}

cd ${BASE_PATH}/${2}
if [ $? -ne 0 ]; then
	exit 1
fi

for infile in ${3}
do
	outfile=`sed -e 's#.*/\(\)#\1#' <<< "$infile"`
	ncks -a -h -O $infile $outfile
	if [ $? -ne 0 ]; then
		exit 2
	fi
done

ncrcat -O -v ${4} ${BASE_PATH}/${2}/*.nc ${BASE_PATH}/${2}.nc
if [ $? -ne 0 ]; then
	exit 3
fi

cd ${BASE_PATH}
if [ $? -ne 0 ]; then
	exit 4
fi

rm -rf ${BASE_PATH}/${2}

exit 0

