import sys
import os

class MetaImporter:
    def find_on_path(self, fullname):
        fls = ["%s/__init__.hy", "%s.hy"]
        dirpath = "/".join(fullname.split("."))

        for pth in sys.path:
            pth = os.path.abspath(pth)
            for fp in fls:
                composed_path = fp % (f"{pth}/{dirpath}")

                if os.path.exists(composed_path):
                    return composed_path
                
    def find_module(self, fullname, path=None):
        path = self.find_on_path(fullname)
        if path:
            return MetaLoader(path)
        

class MetaLoader:
    def __init__(self, path):
        self.path = path

    def is_package(self, fullname:str):
        dirpath = "/".join(fullname.split("."))
        for pth in sys.path:
            pth = os.path.abspath(pth)
            composed_path = f"{pth}/{dirpath}/__init__.hy"
            if os.path.exists(composed_path):
                return True
        return False
    
    def load_module(self, fullname:str):
        if fullname in sys.modules:
            return sys.modules[fullname]
        if not self.path:
            return
        
        sys.modules[fullname] = None
        mod = import_file_to_module(fullname, self.path)

        ispkg = self.is_package(fullname)

        mod.__file__ = self.path
        mod.__loader__ = self
        mod.__name__ = fullname

        if ispkg:
            mod.__path__ = []
            mod.__package__ = fullname
        else:
            mod.__package__ = fullname.rpartition('.')[0]
    
        sys.modules[fullname] = mod
        return mod

sys.meta_path.append(MetaImporter())