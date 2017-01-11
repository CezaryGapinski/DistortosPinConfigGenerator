import json
import jinja2

from pprint import pprint

with open('data.json') as data_file:    
    data = json.load(data_file)
print(data["output_pins"][0]["id"])

print(len(data["output_pins"]))

templateLoader = jinja2.FileSystemLoader( searchpath="." )
templateEnv = jinja2.Environment( loader=templateLoader )

TEMPLATE_FILE = "example.jinja"
template = templateEnv.get_template( TEMPLATE_FILE )

leds_ids = []
leds_id_to_out_pin_ids = []
leds_pins = []

for x in data["leds"]:
  leds_ids.append(x["id"])

for x in data["leds"]:
  leds_id_to_out_pin_ids.append(x["output_pin"])

for x in leds_id_to_out_pin_ids:
  for y in data["output_pins"]:
    if y["id"] == x:
      leds_pins.append(y["pin"])
	

templateVars = { "board" : data["board"],
                 "gpio_version" : data["gpio_driver_version"],
		 "leds_number" : len(data["leds"]),
		 "leds_ids" : leds_ids,
		 "leds_pins" : leds_pins
               }

# Here we add a new input variable containing a list.
# Its contents will be expanded in the HTML as a unordered list.
#FAVORITES = [ "chocolates", "lunar eclipses", "rabbits" ]

#templateVars = { "title" : "Test Example",
#                 "description" : "A simple inquiry of function.",
#                 "favorites" : FAVORITES
#               }

outputText = template.render( templateVars )

f1=open('./leds.hpp', 'w+')
f1.write(outputText)
print(outputText)
