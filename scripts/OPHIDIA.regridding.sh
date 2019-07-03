#!/bin/bash

# Input parameters
# 1: output path
# 2: output filename
# 3: input file
# 4: geographic subset for latitude (e.g. 30:45)
# 5: geographic subset for longitude (e.g. 0:40)
# 6: grid of output map using the format r<lon>x<lat> (e.g. r360x180)

FileName=${3}
LatRange=${4}
LonRange=${5}
NewGrid=${6}

DataPath=${OPH_SCRIPT_DATA_PATH}/${1}

cd $DataPath
if [ $? -ne 0 ]; then
	exit 1
fi

infile=$FileName
outfile=`sed -e 's#.*/\(\)#\1#' <<< "$infile"`
ncks -a -h -O $infile $outfile
if [ $? -ne 0 ]; then
	exit 2
fi
InFile=$DataPath/$outfile

LATS=180
LONS=360

# Bilinear regridding
if [ "$NewGrid" != "" ]; then

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
	mv $tmp $DataPath/${2}.nc

	rm -f $DataPath/.grid

fi

exit 0

