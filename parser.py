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

if (len(sys.argv) != 2):
    print "You must set argument!!!"
    sys.exit(2)
    
cmdargs_path = str(sys.argv[1])

with open('pin_config.json') as data_file:    
    data = json.load(data_file)

templateLoader = jinja2.FileSystemLoader( searchpath="." )
templateEnv = jinja2.Environment( loader=templateLoader )

LEDS_HPP_TEMPLATE = "leds_hpp.jinja"
LEDS_CPP_TEMPLATE = "leds_cpp.jinja"

SPIS_HPP_TEMPLATE = "spi_hpp.jinja"
SPIS_CPP_TEMPLATE = "spi_cpp.jinja"

LOW_LEVEL_PIN_INIT_CPP_TEMPLATE = "lowLevelPinInitialization_cpp.jinja"

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
      
      
pins_type = set()
for x in data["output_pins"]:
    pin_without_number = str(x["pin"])
    pins_type.add(pin_without_number.translate(None, digits))
    
for x in data["alternative_pins"]:
    pin_without_number = str(x["pin"])
    pins_type.add(pin_without_number.translate(None, digits))

for x in pins_type:   
    print(x)
      
templateVars = {    "board" : data["board"],
                    "gpio_version" : data["gpio_driver_version"],
		            "leds_number" : len(data["leds"]),
                    "leds_ids" : leds_ids,
                    "leds_pins" : leds_pins,
                    "spis_number" : len(data["spis_pins"]),
                    "spi_pins_list" : spilist,
                    "used_pins_groups" : pins_type
               }

include_directory = cmdargs_path + "include/distortos/board"

if not os.path.exists(include_directory):
    os.makedirs(include_directory)

template = templateEnv.get_template( LEDS_HPP_TEMPLATE )
outputText = template.render( templateVars )

filename = include_directory + "/" + "%s.hpp" % "leds"
file=open(filename, 'w')
file.write(outputText)
file.close()

template = templateEnv.get_template( LEDS_CPP_TEMPLATE )
outputText = template.render( templateVars )

filename = cmdargs_path + "%s.cpp" % (data["board"] + "-leds")
file=open(filename, 'w')
file.write(outputText)
file.close()

template = templateEnv.get_template( SPIS_HPP_TEMPLATE )
outputText = template.render( templateVars )

filename = include_directory + "/" + "%s.hpp" % "spi"
file=open(filename, 'w')
file.write(outputText)
file.close()

template = templateEnv.get_template( SPIS_CPP_TEMPLATE )
outputText = template.render( templateVars )

filename = cmdargs_path + "%s.cpp" % (data["board"] + "-spi")
file=open(filename, 'w')
file.write(outputText)
file.close()

template = templateEnv.get_template( LOW_LEVEL_PIN_INIT_CPP_TEMPLATE )
outputText = template.render( templateVars )

filename = cmdargs_path + "%s.cpp" % (data["board"] + "-lowLevelPinInitialization")
file=open(filename, 'w')
file.write(outputText)
file.close()

