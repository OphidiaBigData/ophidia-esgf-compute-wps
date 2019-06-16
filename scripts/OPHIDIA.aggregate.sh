#!/bin/bash

cd ${2}
ncrcat ${1} ${2}/${3}.nc

exit 0

