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

output_templates = {}
input_pin_template_path = {}
output_pin_template_path = {}
            
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
    global input_pin_template_path
    global output_pin_template_path
    templateLoader = jinja2.FileSystemLoader([".", os.path.dirname(template_file)])
    templateEnv = jinja2.Environment( loader=templateLoader )
    
    source = templateEnv.loader.get_source(templateEnv, template_file)[0]
    parsed_source = templateEnv.parse(source)
    variables = meta.find_undeclared_variables(parsed_source)
    str_variables2 = str(variables).split('\'')
    
    #check if one of splited variables contain substring output_template
    res = [y for y in str_variables2 if 'output_template' in y]
    if (res):
        output_templates[getOutputFileName(template_file)] = template_file
        
    #check if one of splited variables contain substring input_pin_template
    res = [y for y in str_variables2 if 'input_pin_template' in y]
    if (res):
        split_res = str(res).split('__')
        split_res[1] = split_res[1][:-2]
        if (input_pin_template_path.has_key(split_res[1])):
            raise ValueError("input_pin_template for specified version assigned more than once!")
        else:
            input_pin_template_path[split_res[1]] = template_file
            
    #check if one of splited variables contain substring output_pin_template
    res = [y for y in str_variables2 if 'output_pin_template' in y]
    if (res):
        split_res = str(res).split('__')
        split_res[1] = split_res[1][:-2]
        if (output_pin_template_path.has_key(split_res[1])):
            raise ValueError("output_pin_template for specified version assigned more than once!")
        else:
            output_pin_template_path[split_res[1]] = template_file
                    
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
        if (data["leds"]):
            collectLedsTemplateParams(template_vars, data)
            template_vars["used_pins_groups_leds"] = collectPinGroupsTemplateParams(template_vars["leds_pins"])
            
        if (data["buttons"]):
            collectButtonsTemplateParams(template_vars, data)
            template_vars["used_pins_groups_buttons"] = collectPinGroupsTemplateParams(template_vars["buttons_pins"])
        
        if (data["gpio_driver_version"]):
            template_vars["gpio_input_template"] = input_pin_template_path[data["gpio_driver_version"]]
            template_vars["gpio_output_template"] = output_pin_template_path[data["gpio_driver_version"]]
            template_vars["gpio_version"] = data["gpio_driver_version"]        
    
        template_vars[key] = data[key]
       
    filename = ""
    for key, value in output_templates.iteritems():
        key = replaceBoardStringInFileName(key, template_vars["board"])
        if(isFileTypeHpp(key)):
            filename = include_directory + "/" + key
        else:
            filename = output_board_path + key
        generateJinja2File(filename, value, template_vars)

if __name__ == '__main__': main()
