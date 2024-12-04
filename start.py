import unittest
import FunctionList
import pytest
from os.path import dirname
from os.path import realpath
import sys
import time
import shutil
import os
#-----------------------------Read Arguments----------------------------------------
import argparse
parser = argparse.ArgumentParser(description='Run automated functional tests.')
#parser.add_argument('-r','--ring', type=str, help='Ring under test (canary,ida,external)',required=False)
parser.add_argument('-w','--webdriverpath', type=str, help='Path to the webdriver. If excluded, assumes PATH.',required=False)
parser.add_argument('-m','--modelName', type=str, help='Model to be tested',required=False)
parser.add_argument('-l','--link', type=str, help='link to be tested',required=False)
parser.add_argument('-v','--version', type=str, help='version to the test app',required=False)
parser.add_argument('-t','--modelType', type=str, help='type of Model to be tested (3D or Ortho or PointCloud)',required=True)

args = parser.parse_args()


	
def main():
	
	folder = dirname(realpath(sys.argv[0]))
	model_types=args.modelType.split(',') # split the string by comma into a list of values
	if(os.path.exists('%s/Results' % folder)):
		shutil.rmtree('%s/Results' %folder)
	os.mkdir("%s/Results" % folder)
	if(os.path.exists('%s/Difference' % folder)):
		shutil.rmtree('%s/Difference' %folder)
	os.mkdir("%s/Difference" % folder)
	if(os.path.exists('%s/Failures' % folder)):
		shutil.rmtree('%s/Failures' %folder)
	os.mkdir("%s/Failures" % folder)
	for i in model_types:
		version=args.version
		print("GVC version   : "+version)
		if (i.upper() == "3D"):
			testsPath = "%s/test_cases/3D" % folder
			if(args.modelName == None):
				args.modelName = "3D-Refining (File)"
		elif (i.upper() == "POINTCLOUD"):
			testsPath = "%s/test_cases/PointCloud" % folder
			if(args.modelName == None):
				args.modelName = "3D-Matterport HSPC (File)"
		elif (i.upper() == "COMBINED"):
			testsPath = "%s/test_cases/Combined" % folder
			if(args.modelName == None):
				args.modelName = "3D-Combined-parametric (File)"
		elif (i.upper() == "2D"):
			testsPath = "%s/test_cases/2D" % folder
			if(args.modelName == None):
				args.modelName = "2D-Radix PID SAM (GDS Extern)"
		elif (i.upper() == "2DC"):
			testsPath = "%s/test_cases/2DC" % folder
			if(args.modelName == None):
				args.modelName = "2D-Radix PID SAM (GDS Extern)"		
		elif (i.upper() == "2DS"):
			testsPath = "%s/test_cases/2DS" % folder
			if(args.modelName == None):
				args.modelName = "2D-Radix PID SAM (GDS Extern)"			
		else:
			assert False, "Please provide either of 3D or 2D or Combined or PointCloud as modelType"		
		print("Model name    : "+args.modelName)
		print("Tests location: "+testsPath)
		pytest.model = args.modelName
		failuresput = "{}/Results/results_{}.xml".format(folder, i)
		FunctionList.setup(args)
		try:
			FunctionList.initialize()	
		except:
			FunctionList.snapshot("initialize")
			raise
		try:
			print("Starting test cases")
			pytest.main(["--tb=short","--junitxml", failuresput,testsPath])
		except Exception as e:
			print(e)
		finally:
			FunctionList.finishTests() # close driver and clean up
			args.modelName=None
			 	
if __name__ == "__main__":
	main()