#!/bin/bash

#GetCapabilities
curl -k -L -X GET "https://0.0.0.0/wps/?request=GetCapabilities&service=WPS&version=1.0.0" -H 'cache-control: no-cache'

#OPHIDIA.subset
curl -k -L -X GET "https://0.0.0.0/wps/?request=Execute&service=WPS&version=1.0.0&identifier=OPHIDIA.subset&datainputs=variable%3D%5B%7B%22uri%22%3A%22file.nc%22%2C%22id%22%3A%22tos%7Cv1%22%2C%22domain%22%3A%22d0%22%7D%5D%3Bdomain%3D%5B%7B%22lat%22%3A%7B%22start%22%3A-60%2C%22end%22%3A-15%2C%22crs%22%3A%22values%22%7D%2C%22lon%22%3A%7B%22start%22%3A42%2C%22end%22%3A113%2C%22crs%22%3A%22values%22%7D%2C%22id%22%3A%22d0%22%7D%5D%3Boperation%3D%5B%7B%22name%22%3A%22OPHIDIA.subset%22%2C%22input%22%3A%5B%22v1%22%5D%2C%22domain%22%3A%22d0%22%2C%22axes%22%3A%22time%22%7D%5D" -H 'cache-control: no-cache'

#OPHIDIA.max
curl -k -L -X GET "https://0.0.0.0/wps/?request=Execute&service=WPS&version=1.0.0&identifier=OPHIDIA.max&datainputs=variable%3D%5B%7B%22uri%22%3A%22file.nc%22%2C%22id%22%3A%22tos%7Cv1%22%2C%22domain%22%3A%22d0%22%7D%5D%3Bdomain%3D%5B%7B%22lat%22%3A%7B%22start%22%3A-60%2C%22end%22%3A-15%2C%22crs%22%3A%22values%22%7D%2C%22lon%22%3A%7B%22start%22%3A42%2C%22end%22%3A113%2C%22crs%22%3A%22values%22%7D%2C%22id%22%3A%22d0%22%7D%5D%3Boperation%3D%5B%7B%22name%22%3A%22OPHIDIA.max%22%2C%22input%22%3A%5B%22v1%22%5D%2C%22domain%22%3A%22d0%22%2C%22axes%22%3A%22time%22%7D%5D" -H 'cache-control: no-cache'

#OPHIDIA.min
curl -k -L -X GET "https://0.0.0.0/wps/?request=Execute&service=WPS&version=1.0.0&identifier=OPHIDIA.min&datainputs=variable%3D%5B%7B%22uri%22%3A%22file.nc%22%2C%22id%22%3A%22tos%7Cv1%22%2C%22domain%22%3A%22d0%22%7D%5D%3Bdomain%3D%5B%7B%22lat%22%3A%7B%22start%22%3A-60%2C%22end%22%3A-15%2C%22crs%22%3A%22values%22%7D%2C%22lon%22%3A%7B%22start%22%3A42%2C%22end%22%3A113%2C%22crs%22%3A%22values%22%7D%2C%22id%22%3A%22d0%22%7D%5D%3Boperation%3D%5B%7B%22name%22%3A%22OPHIDIA.min%22%2C%22input%22%3A%5B%22v1%22%5D%2C%22domain%22%3A%22d0%22%2C%22axes%22%3A%22time%22%7D%5D" -H 'cache-control: no-cache'

#OPHIDIA.avg
curl -k -L -X GET "https://0.0.0.0/wps/?request=Execute&service=WPS&version=1.0.0&identifier=OPHIDIA.avg&datainputs=variable%3D%5B%7B%22uri%22%3A%22file.nc%22%2C%22id%22%3A%22tos%7Cv1%22%2C%22domain%22%3A%22d0%22%7D%5D%3Bdomain%3D%5B%7B%22lat%22%3A%7B%22start%22%3A-60%2C%22end%22%3A-15%2C%22crs%22%3A%22values%22%7D%2C%22lon%22%3A%7B%22start%22%3A42%2C%22end%22%3A113%2C%22crs%22%3A%22values%22%7D%2C%22id%22%3A%22d0%22%7D%5D%3Boperation%3D%5B%7B%22name%22%3A%22OPHIDIA.avg%22%2C%22input%22%3A%5B%22v1%22%5D%2C%22domain%22%3A%22d0%22%2C%22axes%22%3A%22time%22%7D%5D" -H 'cache-control: no-cache'

#OPHIDIA.aggregate
curl -k -L -X GET "https://0.0.0.0/wps/?request=Execute&service=WPS&version=1.0.0&identifier=OPHIDIA.aggregate&datainputs=variable%3D%5B%7B%22uri%22%3A%22file.nc%20file.nc%22%2C%22id%22%3A%22tos%7Cv1%22%2C%22domain%22%3A%22d0%22%7D%5D%3Bdomain%3D%5B%7B%22lat%22%3A%7B%22start%22%3A-60%2C%22end%22%3A-15%2C%22crs%22%3A%22values%22%7D%2C%22lon%22%3A%7B%22start%22%3A42%2C%22end%22%3A113%2C%22crs%22%3A%22values%22%7D%2C%22id%22%3A%22d0%22%7D%5D%3Boperation%3D%5B%7B%22name%22%3A%22OPHIDIA.aggregate%22%2C%22input%22%3A%5B%22v1%22%5D%2C%22domain%22%3A%22d0%22%2C%22axes%22%3A%22time%22%7D%5D" -H 'cache-control: no-cache'


