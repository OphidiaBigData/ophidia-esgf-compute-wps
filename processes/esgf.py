#
#    Ophidia ESGF Compute WPS Module
#    Copyright (C) 2015-2019 CMCC Foundation
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from pywps import Process, LiteralInput, LiteralOutput
from PyOphidia import cube
from esgfinput import *
import subprocess
import logging
import uuid
import yaml

LOGGER = logging.getLogger("PYWPS")

# Const
_version = "1.0.0"
_username = "oph-test"
_password = "abcd"
_configuration_file = "/usr/local/ophidia/extra/wps/config.yml"

# Configuration options
with open(_configuration_file, 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
setting_host = cfg['setting_host']
setting_port = cfg['setting_port']
setting_outputpath = cfg['setting_outputpath']
setting_outputurl = cfg['setting_outputurl']

class oph_esgf_subset(Process):

    def __init__(self):

        inputs = []
        outputs = []

        variable = LiteralInput(
            'variable',
            'Variable',
            abstract="Variable list",
            data_type='string')

        domain = LiteralInput(
            'domain',
            'Domain',
            abstract="Domain list",
            data_type='string')

        operation = LiteralInput(
            'operation',
            'Operation list',
            abstract="Operation list",
            data_type='string')

        response = LiteralOutput(
            'response',
            'Response',
            abstract="Response",
            data_type='string')

        inputs = [variable, domain, operation]
        outputs = [response]

        super(oph_esgf_subset, self).__init__(
            self._handler,
            identifier='OPHIDIA.subset',
            title='OPHIDIA.subset',
            abstract="An Ophidia ESGF CWT operator used to extract a subset from a dataset",
            version=_version,
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):

        response.update_status("Pre-processing", 1)

        response.outputs['response'].data = ""

        variables_as_string = request.inputs['variable'][0].data
        domains_as_string = request.inputs['domain'][0].data
        operations_as_string = request.inputs['operation'][0].data

        LOGGER.debug("Variable list: %s" % variables_as_string)
        LOGGER.debug("Domain list: %s" % domains_as_string)
        LOGGER.debug("Operation list: %s" % operations_as_string)
        
        domains_as_string = request.inputs['domain'][0].data
        variables_as_string = request.inputs['variable'][0].data
        operations_as_string = request.inputs['operation'][0].data

        inputString = ''
        if domains_as_string:
            inputString = inputString + 'domain=' + domains_as_string + ';'
        if variables_as_string:
            inputString = inputString + 'variable=' + variables_as_string + ';'
        if operations_as_string:
            inputString = inputString + 'operation=' + operations_as_string + ';'

        LOGGER.debug("Command: %s" % inputString)

        esgf = EsgfInput(inputString)

        domains = esgf.getDomains()
        variables = esgf.getVariables()
        operations = esgf.getOperations()

        response.update_status("Running", 2)

        v = variables[0]
        input_variable = v.id
        input_uri = v.uri
        input_domain = v.domain
        for d in domains:
            if d.id == input_domain:
                working_domain = d
                dimensions = working_domain.dimensions
            else:
                LOGGER.debug("Variable {} points at no passed domain" % format(v.id))

        dimension_names = list(dimensions)

        input_subset_dims = ''
        for dimension_name in dimension_names:
            input_subset_dims = input_subset_dims + dimension_name
            if dimension_name != dimension_names[-1]:
                input_subset_dims = input_subset_dims + '|'

        input_subset_filter = ''
        for dimension_name in dimension_names:
            start = str(dimensions[dimension_name]['start'])
            end = str(dimensions[dimension_name]['end'])
            input_subset_filter = input_subset_filter + start + ':' + end
            if dimension_name != dimension_names[-1]:
                input_subset_filter = input_subset_filter + '|'

        input_subset_type = ''
        for dimension_name in dimension_names:
            crs = str(dimensions[dimension_name]['crs'])
            if crs == 'values':
                crs = 'coord'
            input_subset_type = input_subset_type + crs
            if dimension_name != dimension_names[-1]:
                input_subset_type = input_subset_type + '|'

        input_dimensions = 'time' # Dimension along reduction is done

        LOGGER.debug("Execute the job")

        out_name = str(uuid.uuid4())

        cube.Cube.setclient(username=_username, password=_password, server=setting_host, port=setting_port)
        cube1 = cube.Cube.importnc(imp_dim=input_dimensions, measure=input_variable, src_path=input_uri, subset_dims=input_subset_dims, subset_filter=input_subset_filter, subset_type=input_subset_type)
        cube1.exportnc2(output_path=setting_outputpath, output_name=out_name)
        cube1.delete()

        out_link = setting_outputurl + '/' + out_name + '.nc'
        
        LOGGER.debug("Response: %s" % out_link)

        response.update_status("Post-processing", 99)

        if len(out_link) > 0:
            response.outputs['response'].data = out_link

        response.update_status("Succeded", 100)

        return response

class oph_esgf_max(Process):

    def __init__(self):

        inputs = []
        outputs = []

        variable = LiteralInput(
            'variable',
            'Variable',
            abstract="Variable list",
            data_type='string')

        domain = LiteralInput(
            'domain',
            'Domain',
            abstract="Domain list",
            data_type='string')

        operation = LiteralInput(
            'operation',
            'Operation list',
            abstract="Operation list",
            data_type='string')

        response = LiteralOutput(
            'response',
            'Response',
            abstract="Response",
            data_type='string')

        inputs = [variable, domain, operation]
        outputs = [response]

        super(oph_esgf_max, self).__init__(
            self._handler,
            identifier='OPHIDIA.max',
            title='OPHIDIA.max',
            abstract="An Ophidia ESGF CWT operator used to evaluate the maximum value of a dataset",
            version=_version,
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):

        response.update_status("Pre-processing", 1)

        response.outputs['response'].data = ""

        variables_as_string = request.inputs['variable'][0].data
        domains_as_string = request.inputs['domain'][0].data
        operations_as_string = request.inputs['operation'][0].data

        LOGGER.debug("Variable list: %s" % variables_as_string)
        LOGGER.debug("Domain list: %s" % domains_as_string)
        LOGGER.debug("Operation list: %s" % operations_as_string)
        
        domains_as_string = request.inputs['domain'][0].data
        variables_as_string = request.inputs['variable'][0].data
        operations_as_string = request.inputs['operation'][0].data

        inputString = ''
        if domains_as_string:
            inputString = inputString + 'domain=' + domains_as_string + ';'
        if variables_as_string:
            inputString = inputString + 'variable=' + variables_as_string + ';'
        if operations_as_string:
            inputString = inputString + 'operation=' + operations_as_string + ';'

        LOGGER.debug("Command: %s" % inputString)

        esgf = EsgfInput(inputString)

        domains = esgf.getDomains()
        variables = esgf.getVariables()
        operations = esgf.getOperations()

        response.update_status("Running", 2)

        v = variables[0]
        input_variable = v.id
        input_uri = v.uri
        input_domain = v.domain
        for d in domains:
            if d.id == input_domain:
                working_domain = d
                dimensions = working_domain.dimensions
            else:
                LOGGER.debug("Variable {} points at no passed domain" % format(v.id))

        dimension_names = list(dimensions)

        input_subset_dims = ''
        for dimension_name in dimension_names:
            input_subset_dims = input_subset_dims + dimension_name
            if dimension_name != dimension_names[-1]:
                input_subset_dims = input_subset_dims + '|'

        input_subset_filter = ''
        for dimension_name in dimension_names:
            start = str(dimensions[dimension_name]['start'])
            end = str(dimensions[dimension_name]['end'])
            input_subset_filter = input_subset_filter + start + ':' + end
            if dimension_name != dimension_names[-1]:
                input_subset_filter = input_subset_filter + '|'

        input_subset_type = ''
        for dimension_name in dimension_names:
            crs = str(dimensions[dimension_name]['crs'])
            if crs == 'values':
                crs = 'coord'
            input_subset_type = input_subset_type + crs
            if dimension_name != dimension_names[-1]:
                input_subset_type = input_subset_type + '|'

        input_dimensions = 'time' # Dimension along reduction is done

        LOGGER.debug("Execute the job")

        out_name = str(uuid.uuid4())

        cube.Cube.setclient(username=_username, password=_password, server=setting_host, port=setting_port)
        cube1 = cube.Cube.importnc(imp_dim=input_dimensions, measure=input_variable, src_path=input_uri, subset_dims=input_subset_dims, subset_filter=input_subset_filter, subset_type=input_subset_type)
        cube2 = cube1.reduce(operation='max')
        cube1.delete()
        cube2.exportnc2(output_path=setting_outputpath, output_name=out_name)
        cube2.delete()

        out_link = setting_outputurl + '/' + out_name + '.nc'
        
        LOGGER.debug("Response: %s" % out_link)

        response.update_status("Post-processing", 99)

        if len(out_link) > 0:
            response.outputs['response'].data = out_link

        response.update_status("Succeded", 100)

        return response

class oph_esgf_min(Process):

    def __init__(self):

        inputs = []
        outputs = []

        variable = LiteralInput(
            'variable',
            'Variable',
            abstract="Variable list",
            data_type='string')

        domain = LiteralInput(
            'domain',
            'Domain',
            abstract="Domain list",
            data_type='string')

        operation = LiteralInput(
            'operation',
            'Operation list',
            abstract="Operation list",
            data_type='string')

        response = LiteralOutput(
            'response',
            'Response',
            abstract="Response",
            data_type='string')

        inputs = [variable, domain, operation]
        outputs = [response]

        super(oph_esgf_min, self).__init__(
            self._handler,
            identifier='OPHIDIA.min',
            title='OPHIDIA.min',
            abstract="An Ophidia ESGF CWT operator used to evaluate the minimum value of a dataset",
            version=_version,
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):

        response.update_status("Pre-processing", 1)

        response.outputs['response'].data = ""

        variables_as_string = request.inputs['variable'][0].data
        domains_as_string = request.inputs['domain'][0].data
        operations_as_string = request.inputs['operation'][0].data

        LOGGER.debug("Variable list: %s" % variables_as_string)
        LOGGER.debug("Domain list: %s" % domains_as_string)
        LOGGER.debug("Operation list: %s" % operations_as_string)
        
        domains_as_string = request.inputs['domain'][0].data
        variables_as_string = request.inputs['variable'][0].data
        operations_as_string = request.inputs['operation'][0].data

        inputString = ''
        if domains_as_string:
            inputString = inputString + 'domain=' + domains_as_string + ';'
        if variables_as_string:
            inputString = inputString + 'variable=' + variables_as_string + ';'
        if operations_as_string:
            inputString = inputString + 'operation=' + operations_as_string + ';'

        LOGGER.debug("Command: %s" % inputString)

        esgf = EsgfInput(inputString)

        domains = esgf.getDomains()
        variables = esgf.getVariables()
        operations = esgf.getOperations()

        response.update_status("Running", 2)

        v = variables[0]
        input_variable = v.id
        input_uri = v.uri
        input_domain = v.domain
        for d in domains:
            if d.id == input_domain:
                working_domain = d
                dimensions = working_domain.dimensions
            else:
                LOGGER.debug("Variable {} points at no passed domain" % format(v.id))

        dimension_names = list(dimensions)

        input_subset_dims = ''
        for dimension_name in dimension_names:
            input_subset_dims = input_subset_dims + dimension_name
            if dimension_name != dimension_names[-1]:
                input_subset_dims = input_subset_dims + '|'

        input_subset_filter = ''
        for dimension_name in dimension_names:
            start = str(dimensions[dimension_name]['start'])
            end = str(dimensions[dimension_name]['end'])
            input_subset_filter = input_subset_filter + start + ':' + end
            if dimension_name != dimension_names[-1]:
                input_subset_filter = input_subset_filter + '|'

        input_subset_type = ''
        for dimension_name in dimension_names:
            crs = str(dimensions[dimension_name]['crs'])
            if crs == 'values':
                crs = 'coord'
            input_subset_type = input_subset_type + crs
            if dimension_name != dimension_names[-1]:
                input_subset_type = input_subset_type + '|'

        input_dimensions = 'time' # Dimension along reduction is done

        LOGGER.debug("Execute the job")

        out_name = str(uuid.uuid4())

        cube.Cube.setclient(username=_username, password=_password, server=setting_host, port=setting_port)
        cube1 = cube.Cube.importnc(imp_dim=input_dimensions, measure=input_variable, src_path=input_uri, subset_dims=input_subset_dims, subset_filter=input_subset_filter, subset_type=input_subset_type)
        cube2 = cube1.reduce(operation='min')
        cube1.delete()
        cube2.exportnc2(output_path=setting_outputpath, output_name=out_name)
        cube2.delete()
        
        out_link = setting_outputurl + '/' + out_name + '.nc'

        LOGGER.debug("Response: %s" % out_link)

        response.update_status("Post-processing", 99)

        if len(out_link) > 0:
            response.outputs['response'].data = out_link

        response.update_status("Succeded", 100)

        return response

class oph_esgf_avg(Process):

    def __init__(self):

        inputs = []
        outputs = []

        variable = LiteralInput(
            'variable',
            'Variable',
            abstract="Variable list",
            data_type='string')

        domain = LiteralInput(
            'domain',
            'Domain',
            abstract="Domain list",
            data_type='string')

        operation = LiteralInput(
            'operation',
            'Operation list',
            abstract="Operation list",
            data_type='string')

        response = LiteralOutput(
            'response',
            'Response',
            abstract="Response",
            data_type='string')

        inputs = [variable, domain, operation]
        outputs = [response]

        super(oph_esgf_min, self).__init__(
            self._handler,
            identifier='OPHIDIA.avg',
            title='OPHIDIA.avg',
            abstract="An Ophidia ESGF CWT operator used to evaluate the mean value of a dataset",
            version=_version,
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):

        response.update_status("Pre-processing", 1)

        response.outputs['response'].data = ""

        variables_as_string = request.inputs['variable'][0].data
        domains_as_string = request.inputs['domain'][0].data
        operations_as_string = request.inputs['operation'][0].data

        LOGGER.debug("Variable list: %s" % variables_as_string)
        LOGGER.debug("Domain list: %s" % domains_as_string)
        LOGGER.debug("Operation list: %s" % operations_as_string)
        
        domains_as_string = request.inputs['domain'][0].data
        variables_as_string = request.inputs['variable'][0].data
        operations_as_string = request.inputs['operation'][0].data

        inputString = ''
        if domains_as_string:
            inputString = inputString + 'domain=' + domains_as_string + ';'
        if variables_as_string:
            inputString = inputString + 'variable=' + variables_as_string + ';'
        if operations_as_string:
            inputString = inputString + 'operation=' + operations_as_string + ';'

        LOGGER.debug("Command: %s" % inputString)

        esgf = EsgfInput(inputString)

        domains = esgf.getDomains()
        variables = esgf.getVariables()
        operations = esgf.getOperations()

        response.update_status("Running", 2)

        v = variables[0]
        input_variable = v.id
        input_uri = v.uri
        input_domain = v.domain
        for d in domains:
            if d.id == input_domain:
                working_domain = d
                dimensions = working_domain.dimensions
            else:
                LOGGER.debug("Variable {} points at no passed domain" % format(v.id))

        dimension_names = list(dimensions)

        input_subset_dims = ''
        for dimension_name in dimension_names:
            input_subset_dims = input_subset_dims + dimension_name
            if dimension_name != dimension_names[-1]:
                input_subset_dims = input_subset_dims + '|'

        input_subset_filter = ''
        for dimension_name in dimension_names:
            start = str(dimensions[dimension_name]['start'])
            end = str(dimensions[dimension_name]['end'])
            input_subset_filter = input_subset_filter + start + ':' + end
            if dimension_name != dimension_names[-1]:
                input_subset_filter = input_subset_filter + '|'

        input_subset_type = ''
        for dimension_name in dimension_names:
            crs = str(dimensions[dimension_name]['crs'])
            if crs == 'values':
                crs = 'coord'
            input_subset_type = input_subset_type + crs
            if dimension_name != dimension_names[-1]:
                input_subset_type = input_subset_type + '|'

        input_dimensions = 'time' # Dimension along reduction is done

        LOGGER.debug("Execute the job")

        out_name = str(uuid.uuid4())

        cube.Cube.setclient(username=_username, password=_password, server=setting_host, port=setting_port)
        cube1 = cube.Cube.importnc(imp_dim=input_dimensions, measure=input_variable, src_path=input_uri, subset_dims=input_subset_dims, subset_filter=input_subset_filter, subset_type=input_subset_type)
        cube2 = cube1.reduce(operation='avg')
        cube1.delete()
        cube2.exportnc2(output_path=setting_outputpath, output_name=out_name)
        cube2.delete()
        
        out_link = setting_outputurl + '/' + out_name + '.nc'

        LOGGER.debug("Response: %s" % out_link)

        response.update_status("Post-processing", 99)

        if len(out_link) > 0:
            response.outputs['response'].data = out_link

        response.update_status("Succeded", 100)

        return response

