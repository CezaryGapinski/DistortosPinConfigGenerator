import json
import jinja2

from pprint import pprint

with open('pin_config.json') as data_file:    
    data = json.load(data_file)

templateLoader = jinja2.FileSystemLoader( searchpath="." )
templateEnv = jinja2.Environment( loader=templateLoader )

LEDS_HPP_TEMPLATE = "leds_hpp.jinja"
LEDS_CPP_TEMPLATE = "leds_cpp.jinja"

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
      
templateVars = {    "board" : data["board"],
                    "gpio_version" : data["gpio_driver_version"],
		            "leds_number" : len(data["leds"]),
                    "leds_ids" : leds_ids,
                    "leds_pins" : leds_pins
               }

template = templateEnv.get_template( LEDS_HPP_TEMPLATE )
outputText = template.render( templateVars )

file=open('./leds.hpp', 'w')
file.write(outputText)
file.close()

template = templateEnv.get_template( LEDS_CPP_TEMPLATE )
outputText = template.render( templateVars )

file=open('./leds.cpp', 'w')
file.write(outputText)
file.close()

