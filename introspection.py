#!/usr/bin/env python

import types
from numpy import linalg as n

def introspect(list={}, curobj="None", scope=None):
	ecurobj = eval(curobj)
	#print "Testing: ", curobj, " of type: ",  type(ecurobj )
	if ecurobj is None and scope:
		#print "Scope: ",scope
		for item in scope:
			info = introspect(list, item)
			if info:
				#print info
				list.update(info)
		return list
	elif type(ecurobj ) is types.ModuleType:
		#vv-break recursive module definitions-vv
		nscope = []
		objlevels = curobj.split('.')
		for item in dir(ecurobj):
			if item not in objlevels:
				nscope.append("%s.%s"%(curobj,item))
		#^^-------^^
		#print "Child Modules: ",nscope
		return introspect(scope=nscope)
	elif type(ecurobj ) in (types.FunctionType,types.BuiltinFunctionType):
		try:
			return { \
			curobj:{ \
				"arguments":ecurobj.func_code.co_varnames[:ecurobj.func_code.co_argcount],\
				"defaults":ecurobj.func_defaults \
				} \
			}
		except AttributeError:
			return {curobj:{"arguments":-1, "defaults":-1}}
	return None
	
i=introspect(scope=["n"])
for k,v in i.iteritems():
	print "Function: ",k
	print "\tArguments: ",v["arguments"]
	print "\tDefaults: ",v["defaults"]
	print 