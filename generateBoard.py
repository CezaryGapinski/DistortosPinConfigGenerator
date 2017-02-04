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
import jinja2
import os.path
import sys
import getopt
from string import digits

gpio_perihperals_paths = {"v1":"jsonTemplatesGPIOv1",
                          "v2":"jsonTemplatesGPIOv2"
                          }

def checkInputParams(script_name, argv, parameters):
    try:
        opts, args = getopt.getopt(argv, "hc:o:", ["config=", "opath="])
        if (len(sys.argv) < 2): 
            print (script_name + ' -c path/to/config.json -o output/path/')
            sys.exit(2) 
    except getopt.GetoptError:
        print (script_name + ' -c path/to/config.json -o output/path/')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (script_name + ' -c path/to/config.json -o output/path/')
            sys.exit()
        elif opt in ("-c", "--config"):
            parameters[0] = arg
        elif opt in ("-o", "--opath"):
            parameters[1] = arg

def generateJinja2File(filename, template_file, template_vars):
    templateLoader = jinja2.FileSystemLoader( searchpath="." )
    templateEnv = jinja2.Environment( loader=templateLoader )
    
    template = templateEnv.get_template( template_file )
    outputText = template.render( template_vars )
    
    file=open(filename, 'w')
    file.write(outputText)
    file.close()
    
def collectLedsTemplateParams(template_vars, data):
    leds_ids = []
    leds_id_to_out_pin_ids = []
    leds_pins = []
    
    for x in data["leds"]:
      leds_ids.append(x["id"])
    
    for x in data["leds"]:
      leds_id_to_out_pin_ids.append(x["output_pins"])
    
    for x in leds_id_to_out_pin_ids:
      for y in data["output_pins"]:
        if y["id"] == x:
          leds_pins.append(y)
          
    template_vars["leds_number"] = len(data["leds"])
    template_vars["leds_ids"] = leds_ids
    template_vars["leds_pins"] = leds_pins
    
def collectButtonsTemplateParams(template_vars, data):
    buttons_ids = []
    buttons_id_to_in_pin_ids = []
    buttons_pins = []
    
    for x in data["buttons"]:
      buttons_ids.append(x["id"])
    
    for x in data["buttons"]:
      buttons_id_to_in_pin_ids.append(x["input_pins"])
    
    for x in buttons_id_to_in_pin_ids:
      for y in data["input_pins"]:
        if y["id"] == x:
          buttons_pins.append(y)
          
    template_vars["buttons_number"] = len(data["buttons"])
    template_vars["buttons_ids"] = buttons_ids
    template_vars["buttons_pins"] = buttons_pins
    
def collectPinGroupsTemplateParams(template_vars, data):
    pins_type = set()
    for x in data["output_pins"]:
        pin_without_number = str(x["pin"])
        pins_type.add(pin_without_number.translate(None, digits))
        
    for x in data["input_pins"]:
        pin_without_number = str(x["pin"])
        pins_type.add(pin_without_number.translate(None, digits))
        
    template_vars["used_pins_groups"] = pins_type
        
 
def main():
    parameters = ['', '']
    checkInputParams(sys.argv[0], sys.argv[1:], parameters)
        
    with open(parameters[0]) as data_file:    
        data = json.load(data_file)
        
    cmdargs_path = parameters[1]
    cmdargs_path += data["board"] + "/"
   
    gpio_template_dir = gpio_perihperals_paths[data["gpio_driver_version"]]
    
    LEDS_HPP_TEMPLATE = gpio_template_dir + "/leds_hpp.jinja"
    LEDS_CPP_TEMPLATE = gpio_template_dir + "/leds_cpp.jinja"
    
    BUTTONS_HPP_TEMPLATE = gpio_template_dir + "/buttons_hpp.jinja"
    BUTTONS_CPP_TEMPLATE = gpio_template_dir + "/buttons_cpp.jinja"
    
    LOW_LEVEL_PIN_INIT_HPP_TEMPLATE = gpio_template_dir + "/lowLevelPinInitialization_hpp.jinja"
    LOW_LEVEL_PIN_INIT_CPP_TEMPLATE = gpio_template_dir + "/lowLevelPinInitialization_cpp.jinja"
    
    template_vars = {}  
    
    collectLedsTemplateParams(template_vars, data)
    collectButtonsTemplateParams(template_vars, data)
    collectPinGroupsTemplateParams(template_vars, data)    

    template_vars["board"] = data["board"]
    template_vars["template_dir"] = gpio_template_dir
    template_vars["gpio_version"] = data["gpio_driver_version"]
    
    include_directory = cmdargs_path + "include/distortos/board"
    
    if not os.path.exists(include_directory):
        os.makedirs(include_directory)
    
    template_vars["file_type_in_header"] = "LED"   
    filename = include_directory + "/" + "%s.hpp" % "leds"
    generateJinja2File(filename, LEDS_HPP_TEMPLATE, template_vars)
    
    filename = cmdargs_path + "%s.cpp" % (data["board"] + "-leds")
    generateJinja2File(filename, LEDS_CPP_TEMPLATE , template_vars)
    
    template_vars["file_type_in_header"] = "BUTTON"   
    filename = include_directory + "/" + "%s.hpp" % "buttons"
    generateJinja2File(filename, BUTTONS_HPP_TEMPLATE, template_vars)
    
    filename = cmdargs_path + "%s.cpp" % (data["board"] + "-buttons")
    generateJinja2File(filename, BUTTONS_CPP_TEMPLATE , template_vars)
    
    template_vars["file_type_in_header"] = "lowLevelPinInitialization" 
    filename = include_directory + "/" + "%s.hpp" % "lowLevelPinInitialization"
    generateJinja2File(filename, LOW_LEVEL_PIN_INIT_HPP_TEMPLATE , template_vars)
    
    filename = cmdargs_path + "%s.cpp" % (data["board"] + "-lowLevelPinInitialization")
    generateJinja2File(filename, LOW_LEVEL_PIN_INIT_CPP_TEMPLATE , template_vars)
    
    
if __name__ == '__main__': main()