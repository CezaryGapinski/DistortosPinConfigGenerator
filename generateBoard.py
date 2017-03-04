#
# file: DistPinCfgGen.py
# Python script used to generating board configuration files for Distortos embedded operating system
# author: Copyright (C) 2017 Cezary Gapinski cezary.gapinski@gmail.com
# https://github.com/CezaryGapinski/DistortosPinConfigGenerator
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import json
import string
import jinja2
from jinja2 import meta
import argparse
from string import digits
import os
import re

output_templates = {}
            
def inputParams():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                    required=True,
                    action='store',
                    dest='config_file',
                    help='path to json config file')
    parser.add_argument('-o', '--output',
                    required=True,
                    action='store',
                    dest='output_dir_path',
                    help='path to directory where files will be generated')
    parser.add_argument('-s', '--search_path',
                    required=True,
                    action='store',
                    nargs='*',
                    dest='search_path',
                    help='string separated with spaces containt paths where templates are located')
    return parser.parse_args()

def generateJinja2File(filename, template_file, template_vars):
    templateLoader = jinja2.FileSystemLoader([".", os.path.dirname(template_file)])
    templateEnv = jinja2.Environment( loader=templateLoader )
    
    template = templateEnv.get_template( template_file )
    outputText = template.render( template_vars )
        
    out_file=open(filename, 'w')
    out_file.write(outputText)
    out_file.close()
    
def searchForJinja2FilesInPath(paths):
    search_paths = []

    for path in paths: 
        for root, dirs, files in os.walk(path): 
            for file in files: 
                if file.endswith(".jinja"): 
                    search_paths.append(os.path.join(root, file)) 
                
    return search_paths

def collectMetaDataFromJinja2File(template_file):
    global output_templates
    templateLoader = jinja2.FileSystemLoader([".", os.path.dirname(template_file)])
    templateEnv = jinja2.Environment( loader=templateLoader )
    
    source = templateEnv.loader.get_source(templateEnv, template_file)[0]
    parsed_source = templateEnv.parse(source)
    variables = meta.find_undeclared_variables(parsed_source)
    str_variables2 = str(variables).split('\'')
    
    output_templates[template_file] = {}
    for value in str_variables2:
        matchObj = re.match( r'.+?(?=__)', value, re.M|re.I)
        if matchObj:
            output_templates[template_file]['id'] = str(matchObj.group())
            matchObj2 = re.search( r'(?<=)v[0-9]', value, re.M|re.I)
            if matchObj2:
                output_templates[template_file]['version'] = str(matchObj2.group())

def getTemplateFileFromTypeAndVersion(id, version):
    for file_name, parameters in output_templates.iteritems():
        if parameters['id'] == id:
            if (version):
                if (parameters['version'] == version):
                    return file_name
            else:
                return file_name
    return Null

def getOutputFileName(template_file):
    split_val = str(template_file).split("/")
    file_name = split_val[-1].partition(".jinja")
    return file_name[0]

def isFileTypeHpp(file_name):
    return '.hpp' in file_name

def replaceBoardStringInFileName(file_name, board):
    a = file_name
    replace = 'BOARD_NAME'
    withstring = board
    newstr,found,endpart = a.partition(replace)
    
    if found:
        newstr+=withstring+endpart

    return newstr
    
def collectLedsTemplateParams(template_vars, data):
    leds_ids = []
    leds_alternative_ids = []
    leds_id_to_out_pin_ids = []
    leds_pins = []
    leds_pins_group = []
    
    for x in data["leds"]:
        leds_ids.append(x["id"])
        leds_alternative_ids.append(x["alternative_id"])
        leds_id_to_out_pin_ids.append(x["output_pins"])
    
    for x in leds_id_to_out_pin_ids:
        for y in data["output_pins"]:
            if y["id"] == x:
                leds_pins.append(y)
                group = str(y["pin"])
                group = group.translate(None, digits)
                leds_pins_group.append(group[1:])
          
    template_vars["leds_ids"] = zip(leds_ids, leds_alternative_ids, leds_pins_group)
    template_vars["leds_pins"] = leds_pins
    
def collectButtonsTemplateParams(template_vars, data):
    buttons_ids = []
    buttons_id_to_in_pin_ids = []
    buttons_pins = []
    buttons_pins_group = []
    
    for x in data["buttons"]:
        buttons_ids.append(x["id"])
    
    for x in data["buttons"]:
        buttons_id_to_in_pin_ids.append(x["input_pins"])
    
    for x in buttons_id_to_in_pin_ids:
        for y in data["input_pins"]:
            if y["id"] == x:
                buttons_pins.append(y)
                group = str(y["pin"])
                group = group.translate(None, digits)
                buttons_pins_group.append(group[1:])
          
    template_vars["buttons_ids"] = zip(buttons_ids, buttons_pins_group)
    template_vars["buttons_pins"] = buttons_pins
    
def collectPinGroupsTemplateParams(data):
    pins_type = set()
    for x in data:
        pin_without_number = str(x["pin"])
        pin_without_number = pin_without_number.translate(None, digits)
        pins_type.add(pin_without_number[1:])
        
    return pins_type
 
def main():
    input_parameters = inputParams()
    
    jinja_files = searchForJinja2FilesInPath(input_parameters.search_path)

    for file in jinja_files:
        collectMetaDataFromJinja2File(file)

    with open(input_parameters.config_file) as data_file:
        data = json.load(data_file)
        
    output_board_path = input_parameters.output_dir_path
    output_board_path += data["board"] + "/"
    include_board = output_board_path + "include"
    include_directory = output_board_path + "include/distortos/board"
    if not os.path.exists(include_directory):
        os.makedirs(include_directory)
   
    template_vars = {}
    template_vars["board_includes"] = include_board
    
    for key in data:
        if (key == "leds"):
            collectLedsTemplateParams(template_vars, data)
            template_vars["used_pins_groups_leds"] = collectPinGroupsTemplateParams(template_vars["leds_pins"])
            
        elif (key == "buttons"):
            collectButtonsTemplateParams(template_vars, data)
            template_vars["used_pins_groups_buttons"] = collectPinGroupsTemplateParams(template_vars["buttons_pins"])
        
        elif (key == "gpio_driver_version"):
            template_vars["gpio_input_template"] = getTemplateFileFromTypeAndVersion('input_pin_template', data["gpio_driver_version"])
            template_vars["gpio_output_template"] = getTemplateFileFromTypeAndVersion('output_pin_template', data["gpio_driver_version"])
            template_vars["gpio_version"] = data["gpio_driver_version"]
        else:
            template_vars[key] = data[key]
    
    #TODO: when template_path leds, buttons, gpio in out_templ template_path are not defined then remove from out_templ this file
    #because we don't need this file except generate empty when someoune not define it in json file
    filename = ""
    for template_path, parameters in output_templates.iteritems():
        if parameters['id'] == 'output_template':
            filename = replaceBoardStringInFileName(getOutputFileName(template_path), template_vars["board"])
            if(isFileTypeHpp(filename)):
                filename = include_directory + "/" + filename
            else:
                filename = output_board_path + filename
            generateJinja2File(filename, template_path, template_vars)

if __name__ == '__main__': main()
