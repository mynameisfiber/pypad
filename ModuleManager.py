#!/usr/bin/env python

import os
from imp import load_source
#from pypad import loadConfig

class ModuleManager:

  path = []
  modulesList = []
  modules = []

  def __init__(self, config="~/.pypad/modules.conf"):
    #config = pypad.loadConfig(config)
    config = self.readConfig(config)
    self.path = config["path"]
    self.modulesList = config["modules"]
    self.modules = self.loadModules(self.path)
  
  def readConfig(self, config):
    return {"path":["/Users/fiber/Programming/pypad/modules/"],"modules":["Dummy"]}
  
  def loadModules(self,path):
    modules = []
    for loc in path:
      for item in os.listdir(loc):
        name = os.path.split(item)[-1]
        absitem = os.path.join(loc,item)
        if os.path.isdir(item):
          path.append(item)
        elif os.path.isfile(absitem) and name[-2:] == "py" and name[:-3] in self.modulesList:
          modules.append(getattr(load_source(name,absitem),name[:-3])())
    return modules
          
if __name__ == "__main__":
  test = ModuleManager()
  print test.modules
