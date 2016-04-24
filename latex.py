

Latex(object):
	def __init__(self, obj):
		self.obj = obj

	def cmd(self):

		if isinstance(self.obj, Structure):
			if self.obj.text == '':
				return [u"\{name}".format(name = obj.name),'']
			else:
				return [u"\{name}{{text}}".format(name = obj.name, text = obj.text),'']

		if isinstance(self.obj, Package):
			if "package_option" == None:
				return[u"\usepackage{{name}}".format(name = obj.package_name),''])
			else:
				return [u"\usepackage{{name}}[{option}]".format(name = obj.package_name, option = obj.package_option),''])

		if isinstance(self.obj, Bloc):

			pre_name = u"\\" + self.dic["name"]
            if "option" in self.obj.dic.keys():
				pre_name += "[" + self.dic["option"] + "]"
            if "argument" in self.dic.keys():
                pre_name += "{" + self.dic["argument"] + "}"
            if self.dic["env"] == False:
                if "blocs_list" in self.dic.keys():
                	if isinstance(self.dic["blocs_list"], str):
                                                pre_name += "{" + self.dic["blocs_list"]
                                                return [pre_name, "}"]
                                        else:
                                                return [ pre_name + "{", "}"]                                        
               else:
                                pre_name = u"\begin{" + self.dic["name"]+ "}"
                                if "option" in self.dic.keys():
                                        pre_name += "[" + self.dic["option"] + "]"
                                if "argument" in self.dic.keys():
                                        pre_name += "{" + self.dic["argument"] + "}"

                                return [ pre_name, self.dic["blocs_list"], u"\end{" + self.dic["name"]+ "}"]



