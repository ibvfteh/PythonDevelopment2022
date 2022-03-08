import cmd
import pynames
import shlex
import inspect
import pkgutil
import importlib


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string


class Interpreter(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.language = 'native'

        self.generators = {}
        for submodule in pkgutil.iter_modules(pynames.generators.__path__):
            submodule_full_name = 'pynames.generators.' + submodule.name
            module_pointer = importlib.import_module(submodule_full_name)
            tmp_dict = {}
            for class_name, class_reference in inspect.getmembers(module_pointer, inspect.isclass):
                if submodule_full_name == class_reference.__module__:
                    subclass_name = remove_suffix(remove_suffix(
                        remove_suffix(class_name, 'Generator'), 'Names'), 'Fullname')
                    tmp_dict[subclass_name.lower()] = class_reference()
            if len(tmp_dict) == 1:
                self.generators[submodule.name.lower()] = tmp_dict[list(tmp_dict.keys())[0]]
            else:
                self.generators[submodule.name.lower()] = tmp_dict


    def do_language(self, line):
        args = shlex.split(line)
        self.language = args[0] if args[0] in pynames.LANGUAGE.ALL else pynames.LANGUAGE.NATIVE


    def get_prefixes(self, names, prefix):
        return [n for n in names if n.startswith(prefix)]


    def complete_language(self, text, line, begidx, endidx):
        for langs in pynames.LANGUAGE.ALL:
            if lang in line:
                return []
        return get_prefixes(pynames.LANGUAGE.ALL, text)


    def do_generate(self, line):
        args = shlex.split(line)
        generator = self.generators[args[0].lower()]
        if type(generator) == dict:
            generator = generator[args[1].lower()]
        gender = 'f' if 'female' in args else 'm'
        print(generator.get_name_simple(gender, self.language))


    def complete_generate(self, text, line, begidx, endidx):
        genders = ['male', 'female']
        if len(set(genders) & set(shlex.split(line))) != 0:
            return []
        for generator_name, generator in self.generators.items():
            if generator_name in line.lower():
                if type(generator) == dict:
                    for subgenerator_name in generator.keys():
                        if subgenerator_name in line.lower():
                            return self.get_prefixes(genders, text)
                    return self.get_prefixes(list(generator.keys()), text)
                return self.get_prefixes(genders, text)
        return self.get_prefixes(list(self.generators.keys()), text)


    def do_info(self, line):
        args = shlex.split(line)
        generator = self.generators[args[0].lower()]
        if type(generator) == dict:
            generator = generator[args[1].lower()]
        gender = set(args) & set(['female', 'male'])
        if gender:    
            print(generator.get_names_number(list(gender)[0][0]))
        elif len(args) > 2:
            print(*generator.languages)
        else:
            print(generator.get_names_number())

    
    def complete_info(self, text, line, begidx, endidx):
        base = ['male', 'female', 'languages']
        if len(set(base) & set(shlex.split(line))) != 0:
            return []
        for generator_name, generator in self.generators.items():
            if generator_name in line.lower():
                if type(generator) == dict:
                    for subgenerator_name in generator.keys():
                        if subgenerator_name in line.lower():
                            return self.get_prefixes(base, text)
                    return self.get_prefixes(list(generator.keys()), text)
                return self.get_prefixes(base, text)
        return self.get_prefixes(list(self.generators.keys()), text)
        

    def do_exit(self, args):
        return True


Interpreter().cmdloop()
