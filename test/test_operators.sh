#!/bin/bash

manual(){
        echo "Usage:" 
        echo "-o/--operator: operator to test."
        echo "-t/--trial: number of test trials"
        echo "-b/--buffer: time in seconds between each trial; default value=10s"
        echo "-p/--parallel number of parallel trials; default value=0"
        echo "-l/--list: print a list of the available operators"
}

list(){
        echo "Operators available for testing:"
        echo " OPHIDIA.max"
        echo " OPHIDIA.min"
        echo " OPHIDIA.avg"
        echo " OPHIDIA.aggregate"
        echo " OPHIDIA.subset"
        echo " GetCapabilities"
}

# run the test
executeTest(){
        j=$1
        filename=test_$operator_name-$[$j+1].txt
        echo $title >> $filename

        i=0
        while [ $i -lt $trials ]
        do
            echo "$operator_name $[$j+1]: Executing $[$i+1] test trial"
            SECONDS=0
            eval $operator &>/dev/null
            duration=$SECONDS

            echo "trial $[i+1]: $(($duration % 60)) seconds elapsed" >> $filename

            i=$[$i+1]
            if [ $i -ne $trials ]; then
                sleep $buffer
            fi
        done
        echo "$operator_name-$[$j+1] test finished. Results in $filename"
}

#command line arguments
for i in "$@"
do
        case $i in
                -h | --help)
                        manual
                        exit 1
                ;;
                -l | --list)
                        list
                        exit 1
                ;;
                -o=* | --operator)
                        operator_name="${i#*=}" #take the part after the = in the variable i
                ;;
                -t=* | --trials)
                        trials="${i#*=}"
                ;;
                -b=* | --buffer)
                        buffer="${i#*=}"
                ;;
                -p=* | --parallel)
                        parallel="${i#*=}"
                ;;

        esac
done


case $operator_name in

  OPHIDIA.max | max)
    operator="curl -k -L -X GET \"https://192.168.88.108/wps/?request=Execute&service=WPS&version=1.0.0&identifier=OPHIDIA.max&datainputs=variable%3D%5B%7B%22uri%22%3A%22https%3A%2F%2Fophidialab.cmcc.it%2Fthredds%2FdodsC%2Fwps%2Ftest%2Fpr_3hr_CMCC-CM_historical_r1i1p1_200001010130-200012312230.nc%22%2C%22id%22%3A%22pr%7Cv1%22%2C%22domain%22%3A%22d0%22%7D%5D%3Bdomain%3D%5B%7B%22lat%22%3A%7B%22start%22%3A-60%2C%22end%22%3A-15%2C%22crs%22%3A%22values%22%7D%2C%22lon%22%3A%7B%22start%22%3A42%2C%22end%22%3A113%2C%22crs%22%3A%22values%22%7D%2C%22id%22%3A%22d0%22%7D%5D%3Boperation%3D%5B%7B%22name%22%3A%22OPHIDIA.max%22%2C%22input%22%3A%5B%22v1%22%5D%2C%22domain%22%3A%22d0%22%2C%22axes%22%3A%22time%22%7D%5D\" -H 'cache-control: no-cache'"
    operator_name=OPHIDIA.max
    ;;

  OPHIDIA.min | min)
    operator="curl -k -L -X GET \"https://192.168.88.108/wps/?request=Execute&service=WPS&version=1.0.0&identifier=OPHIDIA.min&datainputs=variable%3D%5B%7B%22uri%22%3A%22https%3A%2F%2Fophidialab.cmcc.it%2Fthredds%2FdodsC%2Fwps%2Ftest%2Fpr_3hr_CMCC-CM_historical_r1i1p1_200001010130-200012312230.nc%22%2C%22id%22%3A%22pr%7Cv1%22%2C%22domain%22%3A%22d0%22%7D%5D%3Bdomain%3D%5B%7B%22lat%22%3A%7B%22start%22%3A-60%2C%22end%22%3A-15%2C%22crs%22%3A%22values%22%7D%2C%22lon%22%3A%7B%22start%22%3A42%2C%22end%22%3A113%2C%22crs%22%3A%22values%22%7D%2C%22id%22%3A%22d0%22%7D%5D%3Boperation%3D%5B%7B%22name%22%3A%22OPHIDIA.min%22%2C%22input%22%3A%5B%22v1%22%5D%2C%22domain%22%3A%22d0%22%2C%22axes%22%3A%22time%22%7D%5D\" -H 'cache-control: no-cache'"
    operator_name=OPHIDIA.min
    ;;

  OPHIDIA.avg | avg)
    operator="curl -k -L -X GET \"https://192.168.88.108/wps/?request=Execute&service=WPS&version=1.0.0&identifier=OPHIDIA.avg&datainputs=variable%3D%5B%7B%22uri%22%3A%22https%3A%2F%2Fophidialab.cmcc.it%2Fthredds%2FdodsC%2Fwps%2Ftest%2Fpr_3hr_CMCC-CM_historical_r1i1p1_200001010130-200012312230.nc%22%2C%22id%22%3A%22pr%7Cv1%22%2C%22domain%22%3A%22d0%22%7D%5D%3Bdomain%3D%5B%7B%22lat%22%3A%7B%22start%22%3A-60%2C%22end%22%3A-15%2C%22crs%22%3A%22values%22%7D%2C%22lon%22%3A%7B%22start%22%3A42%2C%22end%22%3A113%2C%22crs%22%3A%22values%22%7D%2C%22id%22%3A%22d0%22%7D%5D%3Boperation%3D%5B%7B%22name%22%3A%22OPHIDIA.avg%22%2C%22input%22%3A%5B%22v1%22%5D%2C%22domain%22%3A%22d0%22%2C%22axes%22%3A%22time%22%7D%5D\" -H 'cache-control: no-cache'"
    operator_name=OPHIDIA.avg
    ;;

  OPHIDIA.aggregate | aggregate)
    operator="curl -k -L -X GET \"https://192.168.88.108/wps/?request=Execute&service=WPS&version=1.0.0&identifier=OPHIDIA.aggregate&datainputs=variable%3D%5B%7B%22uri%22%3A%22https%3A%2F%2Fophidialab.cmcc.it%2Fthredds%2FdodsC%2Fwps%2Ftest%2Fpr_3hr_CMCC-CM_historical_r1i1p1_200001010130-200012312230.nc%20http%3A%2F%2Fophidialab.cmcc.it%2Fthredds%2FdodsC%2Fwps%2Ftest%2Fpr_3hr_CMCC-CM_historical_r1i1p1_200101010130-200112312230.nc%22%2C%22id%22%3A%22pr%7Cv1%22%2C%22domain%22%3A%22d0%22%7D%5D%3Bdomain%3D%5B%7B%22lat%22%3A%7B%22start%22%3A-60%2C%22end%22%3A-15%2C%22crs%22%3A%22values%22%7D%2C%22lon%22%3A%7B%22start%22%3A42%2C%22end%22%3A113%2C%22crs%22%3A%22values%22%7D%2C%22id%22%3A%22d0%22%7D%5D%3Boperation%3D%5B%7B%22name%22%3A%22OPHIDIA.aggregate%22%2C%22input%22%3A%5B%22v1%22%5D%2C%22domain%22%3A%22d0%22%2C%22axes%22%3A%22time%22%7D%5D\" -H 'cache-control: no-cache'"
    operator_name=OPHIDIA.aggregate
    ;;

  OPHIDIA.subset | subset)
    operator="curl -k -L -X GET \"https://192.168.88.108/wps/?request=Execute&service=WPS&version=1.0.0&identifier=OPHIDIA.subset&datainputs=variable%3D%5B%7B%22uri%22%3A%22https%3A%2F%2Fophidialab.cmcc.it%2Fthredds%2FdodsC%2Fwps%2Ftest%2Fpr_3hr_CMCC-CM_historical_r1i1p1_200001010130-200012312230.nc%22%2C%22id%22%3A%22pr%7Cv1%22%2C%22domain%22%3A%22d0%22%7D%5D%3Bdomain%3D%5B%7B%22lat%22%3A%7B%22start%22%3A-60%2C%22end%22%3A-15%2C%22crs%22%3A%22values%22%7D%2C%22lon%22%3A%7B%22start%22%3A42%2C%22end%22%3A113%2C%22crs%22%3A%22values%22%7D%2C%22id%22%3A%22d0%22%7D%5D%3Boperation%3D%5B%7B%22name%22%3A%22OPHIDIA.subset%22%2C%22input%22%3A%5B%22v1%22%5D%2C%22domain%22%3A%22d0%22%2C%22axes%22%3A%22time%22%7D%5D\" -H 'cache-control: no-cache'"
    operator_name=OPHIDIA.subset
    ;;

  GetCapabilities)
    operator="curl -k -L -X GET \"https://192.168.88.108/wps/?request=GetCapabilities&service=WPS&version=1.0.0\" -H 'cache-control: no-cache'"
    operator_name=GetCapabilities
    ;;

  *)
    echo -n "Operator not recognized." 
    echo "$0 -h for usage"
    exit 1
    ;;
esac


if [ -z $operator_name ]; then
        echo "Please specify an operator name: $0 -h for usage" 
        exit 1
fi


if [ -z $trials ]; then
        echo "Please specify a number of testing trials: $0 -h for usage" 
        exit 1
fi


if [ -z $buffer ]; then
        buffer=10
fi


if [ -z $parallel ]; then
        parallel=0
elif [ $parallel -lt 0 ]; then
        echo "Please insert a >=0 value for p"
        exit 1
fi


time=$(date '+%d/%m/%Y_%H:%M:%S')

title="[ $time ] Testing $operator_name - trials: $trials - buffer: $buffer"

if [ $parallel -gt 1 ]; then
    k=0
    while [ $k -lt $parallel ]
    do
        executeTest $k &
        k=$[$k+1]
    done
else
    executeTest 1
fi