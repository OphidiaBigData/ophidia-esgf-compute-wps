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

import re
import ast
import pandas as pd

class Domain(object):
    
    def __init__(self, dict_domain):

        # mandatory parameters. I am sure they are there
        self.id = dict_domain['id']
        self.dimensions = self.__getDimensions(dict_domain)

        # the presence of mask and crs depends from users
        try:
            self.mask = dict_domain['mask']
        except KeyError:
            self.mask = 'not_specified'

        
    def __getDimensions(self, dict_domain):
        dimensions = {}
        
        # key will be the dimension(lat, lon, ...) name
        for key in dict_domain:
            if key not in ('id', 'mask'):
                dimensions[key] = dict_domain[key]
                
                try:
                    dimensions[key]['crs'] = dict_domain[key]['crs']
                except KeyError:
                    dimensions[key]['crs'] = 'not_specified'
        
        dimensions = pd.DataFrame.from_dict(dimensions)
        
        return dimensions
    
    
    def __repr__(self):
        info = '''
          id: {0}
          mask: {1} 
          dimensions: {2}'''.format(self.id, 
                             self.mask,
                             self.dimensions) 
                  
        return "ESGF Input Domain Object \n" + info

#-------------------------------
class Variable(object):
    
    def __init__(self, dict_variable):

        # mandatory parameters. I am sure they are there
        self.uri = dict_variable['uri']
        self.domain = dict_variable['domain']
        self.id = dict_variable['id'].split('|')[0]

        # catch if users specifying an internal id alias
        # e.g. pr|v1
        # in case no alias is provided, splitting the id through |
        # will raise an IndexError. In this case, alias = id
        try:
            self.alias = dict_variable['id'].split('|')[1]
        except IndexError:
            self.alias = self.id
            
    
    def __repr__(self):
        info = '''
          uri: {0}
          domain: {1}
          id: {2}
          alias: {3}'''.format(self.uri, 
                             self.domain, 
                             self.id, 
                             self.alias) 
                  
        return "ESGF Input Variable Object \n" + info
    
#-------------------------------
class Operation(object):
    
    def __init__(self, dict_operation):

        # mandatory parameters. I am sure they are there
        self.name = dict_operation['name']
        self.input = dict_operation['input']
        self.axes = dict_operation['axes'].split('|')
            
    
    def __repr__(self):
        info = '''
          name: {0}
          input: {1}
          axes: {2}'''.format(self.name, 
                             self.input, 
                             self.axes) 
                  
        return "ESGF Input Operation Object \n" + info
    
        
class EsgfInput(object):
    
    def __init__(self, input_string):
        self.__dataInputs = input_string + ';'
        self.__formattedInputs = self.__formatInput()
        self.__dictInput = self.__dictfy()

    def __expandShortcuts(self, data):

        #expanding interval shortcut
        while ".]" in data:
            start = data.find(':[')
            end = data.find('.]', start) +2
            shortcut = data[start:end]
    
            interval = shortcut.replace(":[", "").replace(".]","").replace(".,",",").split(",")
    
            expanded_shorcut = ':{' + '"start":{}'.format(interval[0]) + ',"end":{}'.format(interval[1]) + ',"crs":"values","step":"1"}'

            data = data.replace(shortcut, expanded_shorcut)
        
        #expanding number shortcut
        gex = '("(?!(start|end|step)")\w+":)\s*([.\d]+)'
        data = re.sub(gex, r'\1{"start":\3,"end":\3,"crs":"values","step":"1"}', data)
        return data

    
    def __formatInput(self):
        dataInputs = self.__dataInputs
        
        formattedInputs = re.sub(r'\"input\":\[.*?\]','\"input\":\"\"', dataInputs)

        if 'domain=[' in dataInputs:
            #extract the domain section of the input
            domainInputs = re.findall('domain=\[(.+?)\];', dataInputs)[0]
    
            expanded_domainInputs =self.__expandShortcuts(domainInputs)
    
            #replacing the esgf dimension input names with those of .nc files
            expanded_domainInputs = expanded_domainInputs.replace('longitude','lon').replace('latitude','lat').replace('level','lev')
    
            #replacing the previous domain section with the extended one
            formattedInputs = formattedInputs.replace(domainInputs, expanded_domainInputs)
                
        return formattedInputs
    
    
    def __add_DomainStep(self, dictInputs):
        for subdomain in dictInputs['domain']:
            for key in dictInputs['domain'][subdomain]:
                if key not in ('id','mask'):
                    dimension = key
                    dimension_values = dictInputs['domain'][subdomain][dimension]
                    if 'step' not in list(dimension_values.keys()):
                        dimension_values['step']=1
                        
    
    def __restoreOperationInputs(self, dictInputs):
        
        dataInputs = self.__dataInputs
        
        # retrieving the operation's input list
        raw_list = re.findall('\"input\":\[(.+?)],', dataInputs)
        for sub_key, element in zip(dictInputs['operation'], raw_list):
            # convert each element in a list
            var_list = element.replace("\"","").split(",")
            # assign the list to the operation input
            dictInputs['operation'][sub_key]['input'] = var_list

        return dictInputs


    def __dictfy (self):
        
        dataInputs = self.__dataInputs

        keywords = re.findall(';(.+?)=', ";" + dataInputs)

        formattedInputs = self.__formattedInputs

        dictInputs = {}

        # populating the Dictionary with the dataInputs elements

        # for each keyword
        for key in keywords:
            value = re.findall('{}=\[(.+?)\]'.format(key), formattedInputs)[0]

            # numbers of sub_keywords
            sub_num = value.count(',{')

            # if there are sub_keywords
            if sub_num > 0:

                # create the nested structure: "subkey2":{},...,"subkeyN":{}
                sub_value = value
                for i in range(2,sub_num + 2):

                    # create the sub_keyword name, e.g. domain2
                    sub_key = key + str(i)
                    sub_value = sub_value.replace(',{',',\"{}\":'.format(sub_key)+'{', 1)

                # inserting "subkey1":{} at the beginning
                value = '{\"' + key + '1\":' + sub_value + '}'

            # case of no sub_keywords: create the sub_keyword subkey1
            else:
                sub_value = value
                value = '{\"' + key + '1\":' + sub_value + '}'

            # convert the value and write it into the dictionary, under the keyword "key"
            dictInputs[key] = ast.literal_eval(value)
        
        if 'domain' in dictInputs:
            # adding step=1 as default value
            self.__add_DomainStep(dictInputs)
        
        if 'operation' in dictInputs:
            # putting the initial operation's input list as element
            self.__restoreOperationInputs(dictInputs)

        return dictInputs


    def getDict(self):
        return self.__dictInput


    def getDomains(self):
        domain_list = []
        
        for sub_domain in self.__dictInput['domain']:
            
            values = self.__dictInput['domain'][sub_domain]
            domain = Domain(values)
            domain_list.append(domain)        
            
        return domain_list
    
    
    def getVariables(self):
        variable_list = []
        
        for sub_variable in self.__dictInput['variable']:
            
            values = self.__dictInput['variable'][sub_variable]
            variable = Variable(values)
            variable_list.append(variable)        
            
        return variable_list
    
    
    def getOperations(self):
        operation_list = []
        
        if 'operation' in self.__dictInput:
            for sub_operation in self.__dictInput['operation']:
                
                values = self.__dictInput['operation'][sub_operation]
                operation = Operation(values)
                operation_list.append(operation)        
            
            return operation_list 
        
        
    def __repr__(self):
        d = self.__dictInput
        
        dictstring = 'ESGF Input Object' + '\n'

        def prettyprint (d, indent, dictstring):
            
            for key, value in d.items():
                dictstring = dictstring + '\n' + '  ' * indent + ' ' + str(key)
                
                if isinstance(value, dict):
                    dictstring = prettyprint(value, indent+1, dictstring)
                    
                else:
                    dictstring = dictstring + ': ' + str(value)
            
            return dictstring
        
        dictstring=prettyprint(d, 0, dictstring)
        
        return dictstring
        
