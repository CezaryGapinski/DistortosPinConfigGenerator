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
import shutil
import datetime

outputTemplates = {}

def inputParams():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--config', required=True, action='store', dest='config_file',
			help='path to json config file')
	parser.add_argument('-o', '--output', required=True, action='store', dest='output_dir_path',
			help='path to directory where files will be generated')
	parser.add_argument('-s', '--search_path', required=False, action='store', nargs='*',
			default='.', dest='search_path',
			help='string separated with spaces containt paths where templates are located')
	return parser.parse_args()

def generateJinja2File(filename, templateFile, templateVars):
	templateLoader = jinja2.FileSystemLoader([".", os.path.dirname(templateFile)])
	templateEnv = jinja2.Environment(loader=templateLoader)
	template = templateEnv.get_template(templateFile)
	
	outputText = template.render(templateVars)
	
	outFile=open(filename, 'w')
	outFile.write(outputText)
	outFile.close()

def searchForJinja2FilesInPath(paths):
	searchPaths = []

	for path in paths:
		for root, dirs, files in os.walk(path):
			for file in files:
				if file.endswith(".jinja"):
					searchPaths.append(os.path.join(root, file))

	return searchPaths

def collectMetaDataFromJinja2File(templateFile):
	global outputTemplates
	
	templateLoader = jinja2.FileSystemLoader([".", os.path.dirname(templateFile)])
	templateEnv = jinja2.Environment( loader=templateLoader )
	
	source = templateEnv.loader.get_source(templateEnv, templateFile)[0]
	variables = meta.find_undeclared_variables(templateEnv.parse(source))
	stringFromVarNames = str(variables).split('\'')
	
	outputTemplates[templateFile] = {}
	
	for value in stringFromVarNames:
		matchObj = re.match(r'.+?(?=__)', value, re.M|re.I)
		if matchObj:
			outputTemplates[templateFile]['id'] = str(matchObj.group())
		matchObj = re.search(r'(?<=__)[^}]*(?=__)', value, re.M|re.I)
		if matchObj:
			outputTemplates[templateFile]['type'] = str(matchObj.group())
		matchObj = re.search(r'(?<=__)v[0-9]', value, re.M|re.I)
		if matchObj:
			outputTemplates[templateFile]['version'] = str(matchObj.group())

def getTemplateFileFromTypeAndVersion(id, version):
	for file_name, parameters in outputTemplates.iteritems():
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

def replaceBoardStringInFileName(fileName, boardName):
	newStr,found,endPart = fileName.partition('BOARD_NAME')
	
	if found:
		newStr+=boardName+endPart

	return newStr

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
				matchObj = re.search(r'(?<=p)[^}]?(?=\d{1,2})', str(y["pin"]), re.M|re.I)
				if matchObj:
					leds_pins_group.append(matchObj.group())
	
	template_vars["leds_ids"] = zip(leds_ids, leds_alternative_ids, leds_pins_group)
	template_vars["leds_pins"] = leds_pins

def collectButtonsTemplateParams(template_vars, data):
	buttonsIds = []
	buttonsIdToInPinIds = []
	buttonsPins = []
	buttonsPinsGroup = []
	
	for x in data["buttons"]:
		buttonsIds.append(x["id"])

	for x in data["buttons"]:
		buttonsIdToInPinIds.append(x["input_pins"])

	for x in buttonsIdToInPinIds:
		for y in data["input_pins"]:
			if y["id"] == x:
				buttonsPins.append(y)
				matchObj = re.search(r'(?<=p)[^}]?(?=\d{1,2})', str(y["pin"]), re.M|re.I)
				if matchObj:
					buttonsPinsGroup.append(matchObj.group())
	
	template_vars["buttons_ids"] = zip(buttonsIds, buttonsPinsGroup)
	template_vars["buttons_pins"] = buttonsPins

def collectPinGroupsTemplateParams(data):
	pinsType = set()
	for x in data:
		pinWithoutNumber = str(x["pin"])
		pinWithoutNumber = pinWithoutNumber.translate(None, digits)
		pinsType.add(pinWithoutNumber[1:])

	return pinsType

def removeFromOutputTemplatesIfNotConfiguredParam(input_data):
	for template_path, parameters in outputTemplates.copy().iteritems():
		if 'type' in parameters:
			if not parameters['type'] in input_data:
				del outputTemplates[template_path]

def main():
	inputParameters = inputParams()
	jinjaFiles = searchForJinja2FilesInPath(inputParameters.search_path)

	for file in jinjaFiles:
		collectMetaDataFromJinja2File(file)

	with open(inputParameters.config_file) as data_file:
		data = json.load(data_file)

	outputBoardPath = inputParameters.output_dir_path
	outputBoardPath += data["board"]
	#Remove existing directory
	shutil.rmtree(outputBoardPath, ignore_errors=True)

	outputBoardPath += "/"
	includeBoard = outputBoardPath + "include"
	includeDirectory = outputBoardPath + "include/distortos/board"

	if not os.path.exists(includeDirectory):
		os.makedirs(includeDirectory)

	templateVars = {}
	templateVars["board_includes"] = includeBoard
	templateVars["actual_year"] = datetime.datetime.now().year

	for key in data:
		if (key == "leds"):
			collectLedsTemplateParams(templateVars, data)
			templateVars["used_pins_groups_leds"] = collectPinGroupsTemplateParams(templateVars["leds_pins"])
		elif (key == "buttons"):
			collectButtonsTemplateParams(templateVars, data)
			templateVars["used_pins_groups_buttons"] = collectPinGroupsTemplateParams(templateVars["buttons_pins"])
		elif (key == "gpio_driver_version"):
			templateVars["gpio_input_template"] = getTemplateFileFromTypeAndVersion('input_pin_template',
											data["gpio_driver_version"])
			templateVars["gpio_output_template"] = getTemplateFileFromTypeAndVersion('output_pin_template',
												data["gpio_driver_version"])
			templateVars["gpio_version"] = data["gpio_driver_version"]
		else:
			templateVars[key] = data[key]
	
	removeFromOutputTemplatesIfNotConfiguredParam(data)

	for template_path, parameters in outputTemplates.iteritems():
		if parameters['id'] == 'output_template':
			filename = replaceBoardStringInFileName(getOutputFileName(template_path), templateVars["board"])
			if(isFileTypeHpp(filename)):
				filename = includeDirectory + "/" + filename
			else:
				filename = outputBoardPath + filename
				
			generateJinja2File(filename, template_path, templateVars)

if __name__ == '__main__': main()
