#!/bin/bash

# Input parameters
# 1: base path
# 2: output filename
# 3: list of input file
# 4: input variable

mkdir -p ${1}/${2}

cd ${1}/${2}
if [ $? -ne 0 ]; then
	exit 1
fi

for infile in ${3}
do
	outfile=`sed -e 's#.*/\(\)#\1#' <<< "$infile"`
	ncks -h --no-abc -O $infile $outfile
	if [ $? -ne 0 ]; then
		exit 2
	fi
done

ncrcat -O -v ${4} ${1}/${2}/*.nc ${1}/${2}.nc
if [ $? -ne 0 ]; then
	exit 3
fi

cd ${1}
if [ $? -ne 0 ]; then
	exit 4
fi

rm -rf ${1}/${2}

exit 0

