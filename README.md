Python script used to generating board configuration files for Distortos embedded operating system.
Script uses jinja2 http://jinja.pocoo.org/docs/2.9/ for generating c++ files and JSON file for pins description file.

Usage:
DistPinCfgGen.py -c path/to/config.json -o output/path/

Example of pin configuration can be found in configuration/pin_config.json
