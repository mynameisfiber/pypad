#/usr/bin/env python

#Make interface with function to load config and return array

class Dummy:
  
  keys = []
  window = None
  
  def __init__(self):
    print "Dummy made!"
    return None
    
  def setWindow(self,window):
    self.window = window
    
  def run(self,keypress):
    return None
