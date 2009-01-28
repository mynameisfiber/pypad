#!/usr/bin/env python

import types

class Introspection:

  info = {}

  keys = ["tab"]
  hooks = ["loadFile"]
  window = None
  
  def __init__(self):
    return None
    
  def setWindow(self,window):
    self.window = window
    
  def run(self,keypress):
    return None
    
  def import2(self,name):
      components = name.split('.')
      mod = __import__(components[0])
      for comp in components[1:]:
          mod = getattr(mod, comp)
      return mod
      
  def deepKeySearch(self,needle,hay):
    for k,v in hay.iteritems():
      if type(v) == types.DictType:
        return self.deepKeySearch(needle,v)
      elif k == needle:
        return k

  def populate(self, namespace):
    if not namespace:
      return self.info
    name,importname = namespace.popitem()
    try:
    	object = self.import2(importname)
    	self.info[name] = self.getObjectInformation(object)
    except ImportError:
      print "youch"
      pass
    self.populate(namespace)
    
  def getObjectInformation(self, obj, inpath=""):
    info = {}
    for item in dir(obj):
      path = inpath + "." + item
      nobj = getattr(obj,item)
      if type(nobj) is types.ModuleType:
        #Fix up recursive module definitions
        if inpath.find(item) >= 0:
          info.update({item:self.deepKeySearch(item,self.info)})
        #call function on inner module
        else:
          info.update({item:self.getObjectInformation(nobj,path)})
      elif type(nobj) in (types.FunctionType,types.BuiltinFunctionType):
        try:
          #try to get info about function
          info.update({item:{ \
            "arguments":nobj.func_code.co_varnames[:nobj.func_code.co_argcount],\
            "defaults":nobj.func_defaults \
            } } )
        except AttributeError:
          #default info
          info.update( {item:{"arguments":-1, "defaults":-1}})
    return info
	
if __name__ == '__main__':
  import time
  introspect = Introspection()
  for k,v in [("intro","Introspection")]:
    s = time.time()
    introspect.populate({k:v})
    print introspect.info
    runtime = time.time() - s
    print "Introspected %s in %fs"%(v,runtime)
  # for k,v in i.iteritems():
  #   print "Function: ",k
  #   print "\tArguments: ",v["arguments"]
  #   print "\tDefaults: ",v["defaults"]
  #   print 