#!/bin/bash

# Input parameters
# 1: output path
# 2: output filename without ".nc"
# 3: input file
# 4: geographic subset for latitude (e.g. 30:45)
# 5: geographic subset for longitude (e.g. 0:40)
# 6: grid of output map using the format r<lon>x<lat> (e.g. r360x180)

if [ "${1}" == "" ]; then
	exit 1
fi
if [ "${2}" == "" ]; then
	exit 1
fi
if [ "${3}" == "" ]; then
	exit 1
fi
if [ "${4}" == "" ]; then
	exit 1
fi
if [ "${5}" == "" ]; then
	exit 1
fi
if [ "${6}" == "" ]; then
	exit 1
fi
if [ "${7}" == "" ]; then
	exit 1
fi
if [ "${8}" == "" ]; then
	exit 1
fi

OutputPath=${OPH_SCRIPT_DATA_PATH}/${1}
DataPath=$OutputPath/${2}
FileName=${3}
Tool=${4}
Method=${5}
LatRange=${6}
LonRange=${7}
NewGrid=${8}

cd $OutputPath
if [ $? -ne 0 ]; then
	echo "Folder $OutputPath is not allowed"
	exit 2
fi
if [ "`pwd`" == "/" ]; then
	echo "Wrong parameter error"
	exit 3
fi

mkdir -p $DataPath
cd $DataPath
if [ $? -ne 0 ]; then
	echo "Folder $OutputPath is not allowed"
	exit 2
fi
if [ "`pwd`" == "/" ]; then
	echo "Wrong parameter error"
	exit 3
fi

if [ "$Tool" == "ESMF" ]; then
	echo "Gridder method $Method is not supported yet"
	exit 4
fi

if [ "$Tool" == "CDO" ]; then
	if [ "$Method" != "linear" ]; then
		echo "Gridder method '$Method' is not supported yet"
		exit 4
	fi
fi

infile=$FileName
outfile=`sed -e 's#.*/\(\)#\1#' <<< "$infile"`
ncks -a -h -O $infile $outfile
if [ $? -ne 0 ]; then
	exit 2
fi
InFile=$DataPath/$outfile

if [ "$Tool" == "ESMF" ]; then

fi

if [ "$Tool" == "CDO" ]; then

	LATS=180
	LONS=360

	XSIZE=${NewGrid%%x*}
	XSIZE=${XSIZE##*r}
	YSIZE=${NewGrid##*x}
	XFIRST=${LonRange%%:*}
	YFIRST=${LatRange%%:*}
	XLAST=${LonRange##*:}
	YLAST=${LatRange##*:}
	LATS=`echo "($YLAST)-($YFIRST)" | bc -l`
	LONS=`echo "($XLAST)-($XFIRST)" | bc -l`
	XINC=`echo "($LONS)/($XSIZE)" | bc -l`
	YINC=`echo "($LATS)/($YSIZE)" | bc -l`
	let XSIZE+=1
	let YSIZE+=1

	(
cat <<'EOF'
gridtype = lonlat
xsize = XSIZE
ysize = YSIZE
xfirst = XFIRST
xinc = XINC
yfirst = YFIRST
yinc = YINC
EOF
	) > $DataPath/.grid

	sed -i "s/XSIZE/$XSIZE/g" $DataPath/.grid
	sed -i "s/YSIZE/$YSIZE/g" $DataPath/.grid
	sed -i "s/XFIRST/$XFIRST/g" $DataPath/.grid
	sed -i "s/YFIRST/$YFIRST/g" $DataPath/.grid
	sed -i "s/XINC/$XINC/g" $DataPath/.grid
	sed -i "s/YINC/$YINC/g" $DataPath/.grid

	tmp=$DataPath/.tmp.nc
	cdo remapbil,$DataPath/.grid $InFile $tmp
	mv $tmp $OutputPath/${2}.nc

	cd $OutputPath
	rm -rf $DataPath

fi

exit 0

