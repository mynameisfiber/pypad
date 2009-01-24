#!/usr/bin/env python

from configobj import ConfigObj
from os import path

def readConfig(file="pypad.conf"):
  """Read configuration given by file named `file`.  Thows IOException.
  Returns: ConfigObj"""
  return ConfigObj(file, write_empty_values=True)

def writeConfig(config, file="pypad.conf"):
  """Updates the config `file` with parameters given by `config`.  Throws IOException
  Returns: ConfigObj"""
  if config.filename != file:
    if not path.isfile(file):
      config = ConfigObj(file,create_empty=True,write_empty_values=True)
    else:
      config.filename = file
  config.write()
  return config
  
  
if __name__ == '__main__':
  print readConfig("pypad.conf")