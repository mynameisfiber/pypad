#!/usr/bin/env python

import os
from imp import load_source
import sys

class ModuleManager:

  path = []
  modulesList = []
  modules = []

  def __init__(self, config):
    self.path = [os.path.expanduser(path) for path in config["path"]]
    self.modulesList = config["modules"]
    self.modules = self.loadModules()
    
  def loadModules(self, path=None):
    if not path:
      path = self.path
    oldPath = sys.path
    sys.path = path
    modules = {}
    failedModules = []
    for item in self.modulesList:
      try:
        modules[item.lower()] = getattr(__import__(item),item)()
      except Exception:
        failedModules.append(item)
    sys.path = oldPath
    if failedModules:
      raise Exception("Failed to load modules", failedModules)
    return modules
          
if __name__ == "__main__":
  import config
  test = ModuleManager(config.readConfig()["modules"])
  print test.modules
  print locals()
  print test.modules["introspection"].populate(dir())