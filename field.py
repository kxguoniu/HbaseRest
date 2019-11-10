# -*- coding:utf-8 -*-

__all__ = ["Field", "IntField", "FloatField", "ComplexField", "BoolField",
			"ListField", "TupleField", "StrField", "SetField", "DictField"]

class Field(object):
	def __init__(self, column=None, family=None, qualifier=None, value=None, field_type=None):
		if column:
			if ":" in column:
				family, qualifier = column.split(":", 1)
			else:
				# TODO
				raise
		if family and qualifier:
			self.family = family
			self.qualifier = qualifier
			self.column = ":".join([family, qualifier])
		else:
			# TODO
			raise
		if field_type is None:
			self.field_type = str
		else:
			self.field_type = field_type

		if self.field_type in [int, float, complex, list, tuple, str, set, dict, bool]:
			if value:
				if isinstance(value, self.field_type):
					self.value = self.field_type(value)
				else:
					# TODO
					raise
			else:
				self.value = self.field_type()
		else:
			# TODO
			raise

		# if self.field_type is int:
		# 	pass
		# elif self.field_type is float:
		# 	pass
		# elif self.field_type is complex:
		# 	pass
		# elif self.field_type is list:
		# 	pass
		# elif self.field_type is tuple:
		# 	pass
		# elif self.field_type is str:
		# 	pass
		# elif self.field_type is set:
		# 	pass
		# elif self.field_type is dict:
		# 	pass
		# else:
		# 	# TODO
		# 	raise

	def __str__(self):
		# TODO
		return str(self.value)

	def __repr__(self):
		# TODO
		return str(self.value)

class IntField(Field):
	def __init__(self, column=None, family=None, qualifier=None, value=None):
		super().__init__(column, family, qualifier, value, int)

class FloatField(Field):
	def __init__(self, column=None, family=None, qualifier=None, value=None):
		super().__init__(column, family, qualifier, value, float)

class ComplexField(Field):
	def __init__(self, column=None, family=None, qualifier=None, value=None):
		super().__init__(column, family, qualifier, value, complex)

class BoolField(Field):
	def __init__(self, column=None, family=None, qualifier=None, value=None):
		super().__init__(column, family, qualifier, value, bool)

class ListField(Field):
	def __init__(self, column=None, family=None, qualifier=None, value=None):
		super().__init__(column, family, qualifier, value, list)

class TupleField(Field):
	def __init__(self, column=None, family=None, qualifier=None, value=None):
		super().__init__(column, family, qualifier, value, tuple)

class StrField(Field):
	def __init__(self, column=None, family=None, qualifier=None, value=None):
		super().__init__(column, family, qualifier, value, str)

class SetField(Field):
	def __init__(self, column=None, family=None, qualifier=None, value=None):
		super().__init__(column, family, qualifier, value, set)

class DictField(Field):
	def __init__(self, column=None, family=None, qualifier=None, value=None):
		super().__init__(column, family, qualifier, value, dict)