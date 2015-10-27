#!/usr/bin/env python 

import compiler
from compiler import ast
from compiler.visitor import ExampleASTVisitor
import json

tree = compiler.parseFile('./test.py')

def indentBlock(block):
	lines = block.strip().split('\n')
	return '\t' + '\n\t'.join(lines) + '\n'

def commentBlock(block):
	lines = block.split('\n')
	return '//' + '\n//'.join(lines) + '\n'

class SimpleVisitor:
	def __init__(self):
		self.indent = ''
		self.vars = []
		self.stack = []

	def generate_declarations(self):
		result = ''
		if self.vars:
			result = "var %s;\n" % ', '.join(self.vars) 
		self.vars = self.stack.pop()
		return result

	def visit(self, node, parent=None, indent=False):
		 
		if node is None: return ""

		node_type = node.__class__.__name__

		code = "/* DEFAULT CODE - " + node_type + '*/'

		func_name = 'visit_' + node_type

		fn = getattr(self, func_name, None)

		if fn:
			code = fn(node)
		else:
			print "********Not Handled************"
			print node_type
			print node.__dict__

		if code == None: code = ''

		return code

	def visit_Module(self, node):
		return commentBlock(node.doc) + "\n" + self.visit(node.node)
		# return "/*%s*/\n\n%s" % (node.doc, self.visit(node.node))

	def visit_Stmt(self, node):
		self.stack.append(self.vars)
		self.vars = []
		block = '\n'.join(self.visit(n) for n in node.getChildNodes()) + '\n' 
		
		block = self.generate_declarations() + '\n' + block
		return block

	def visit_Import(self, node):
		return '/* IMPORTS DONT WORK */'

	def visit_Printnl(self, node):
		return "console.log(%s);" % ', '.join(self.visit(n) for n in node.nodes)

	def visit_Const(self, node):
		if isinstance(node.value, basestring):
			return json.dumps(node.value)
		else:
			return repr(node.value)

	def visit_For(self, node):
		name, expr, code, else_part = node.asList()

		body = indentBlock(self.visit(code))
		print body
		return "for (var %s in %s) {\n%s}" % (name.name, self.visit(expr), body)

	def visit_Name(self, node):
		return node.name

	def visit_AssName(self, node):
		return node.name

	def visit_AssAttr(self, node):
		return "%s.%s" % (self.visit(node.expr), node.attrname)

	def visit_Assign(self, node):
		print node.__dict__
		names = []
		for n in node.nodes:
			names.append(self.visit(n))
			# if n.name not in self.vars: self.vars.append(n.name)
			# names.append(n.name)

		return "%s = %s;" % (', '.join(names), self.visit(node.expr))

	def visit_CallFunc(self, node):
		args = []

		for a in node.args:
			args.append(self.visit(a))
		
		return "%s(%s)" % (self.visit(node.node), ', '.join(args))

	def visit_Add(self, node):
		return "%s + %s" % (self.visit(node.left), self.visit(node.right))

	def visit_Getattr(self, node):
		return "%s.%s" % (self.visit(node.expr), node.attrname)

	def visit_Discard(self, node):
		return self.visit(node.expr) + ';'

	def visit_Function(self, node):
		code = indentBlock(self.visit(node.code))
		return "\nfunction %s () {\n%s}" % (node.name, code)

	def visit_Pass(self, node):
		return '// DO NOTHING'

	def visit_Dict(self, node):
		pairs = []
		for t in node.items:
			pairs.append("%s: %s" % (self.visit(t[0]), self.visit(t[1])))
		return "{\n%s}" % indentBlock(',\n'.join(pairs))

	def visit_Return(self, node):
		print node.__dict__
		return "return %s;" % self.visit(node.value)


visitor = SimpleVisitor()
output = visitor.visit(tree)

print "-------------------------------------------"
print output

target = open('./test.js', 'w')
target.truncate()
target.write(output)