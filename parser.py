import json
import jinja2
import os.path
import sys
from string import digits

class spiPins:
    def __init__(self, id, clk, miso, mosi, cs):
        self.id = id
        self.clk = clk
        self.miso = miso
        self.mosi = mosi
        self.cs = cs

def generateJinja2File(filename, templateFile, templateVars):
    template = templateEnv.get_template( templateFile )
    outputText = template.render( templateVars )
    
    file=open(filename, 'w')
    file.write(outputText)
    file.close()

def generateSpiPinsListConfig(data):
    spilist = [ spiPins(0, 0, 0, 0, 0) for i in data["spis_pins"]]     
          
    i = 0
    for x in data["spis_pins"]:
        for y in data["alternative_pins"]:
            if x["clk"] == y["id"]:
                spilist[i].clk = y
                
        for y in data["alternative_pins"]:
            if x["miso"] == y["id"]:
                spilist[i].miso = y
                
        for y in data["alternative_pins"]:
            if x["mosi"] == y["id"]:
                spilist[i].mosi = y
                
        for y in data["output_pins"]:
            if x["cs"] == y["id"]:
                spilist[i].cs = y
                
        spilist[i].id = x["id"]
                
        i += 1
        
    return spilist

if (len(sys.argv) != 2):
    print "You must set argument!!!"
    sys.exit(2)
    
cmdargs_path = str(sys.argv[1])

with open('pin_config.json') as data_file:    
    data = json.load(data_file)

templateLoader = jinja2.FileSystemLoader( searchpath="." )
templateEnv = jinja2.Environment( loader=templateLoader )

LEDS_HPP_TEMPLATE = "templates/leds_hpp.jinja"
LEDS_CPP_TEMPLATE = "templates/leds_cpp.jinja"

BUTTONS_HPP_TEMPLATE = "templates/buttons_hpp.jinja"
BUTTONS_CPP_TEMPLATE = "templates/buttons_cpp.jinja"

SPIS_HPP_TEMPLATE = "templates/spi_hpp.jinja"
SPIS_CPP_TEMPLATE = "templates/spi_cpp.jinja"

LOW_LEVEL_PIN_INIT_HPP_TEMPLATE = "templates/lowLevelPinInitialization_hpp.jinja"
LOW_LEVEL_PIN_INIT_CPP_TEMPLATE = "templates/lowLevelPinInitialization_cpp.jinja"

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
     
spilist = generateSpiPinsListConfig(data) 
      
pins_type = set()
for x in data["output_pins"]:
    pin_without_number = str(x["pin"])
    pins_type.add(pin_without_number.translate(None, digits))
    
for x in data["alternative_pins"]:
    pin_without_number = str(x["pin"])
    pins_type.add(pin_without_number.translate(None, digits))
    
fileTypeInHeader = "EMPTY"

templateVars = {    "board" : data["board"],
                    "file_type_in_header" : fileTypeInHeader,
                    "gpio_version" : data["gpio_driver_version"],
		            "leds_number" : len(data["leds"]),
                    "leds_ids" : leds_ids,
                    "leds_pins" : leds_pins,
                    "buttons_number" : len(data["buttons"]),
                    "buttons_ids" : buttons_ids,
                    "buttons_pins" : buttons_pins,
                    "spis_number" : len(data["spis_pins"]),
                    "spi_pins_list" : spilist,
                    "used_pins_groups" : pins_type
               }

include_directory = cmdargs_path + "include/distortos/board"

if not os.path.exists(include_directory):
    os.makedirs(include_directory)

templateVars["file_type_in_header"] = "LED"   
filename = include_directory + "/" + "%s.hpp" % "leds"
generateJinja2File(filename, LEDS_HPP_TEMPLATE, templateVars)

filename = cmdargs_path + "%s.cpp" % (data["board"] + "-leds")
generateJinja2File(filename, LEDS_CPP_TEMPLATE , templateVars)

templateVars["file_type_in_header"] = "BUTTON"   
filename = include_directory + "/" + "%s.hpp" % "buttons"
generateJinja2File(filename, BUTTONS_HPP_TEMPLATE, templateVars)

filename = cmdargs_path + "%s.cpp" % (data["board"] + "-buttons")
generateJinja2File(filename, BUTTONS_CPP_TEMPLATE , templateVars)

templateVars["file_type_in_header"] = "SPI" 
filename = include_directory + "/" + "%s.hpp" % "spi"
generateJinja2File(filename, SPIS_HPP_TEMPLATE , templateVars)

filename = cmdargs_path + "%s.cpp" % (data["board"] + "-spi")
generateJinja2File(filename, SPIS_CPP_TEMPLATE , templateVars)

templateVars["file_type_in_header"] = "LowLevelPinInitialization" 
filename = include_directory + "/" + "%s.hpp" % "LowLevelPinInitialization"
generateJinja2File(filename, LOW_LEVEL_PIN_INIT_HPP_TEMPLATE , templateVars)

filename = cmdargs_path + "%s.cpp" % (data["board"] + "-lowLevelPinInitialization")
generateJinja2File(filename, LOW_LEVEL_PIN_INIT_CPP_TEMPLATE , templateVars)
