import json


class Namelist(object):
    def __init__(self):
        with open('defaults.json') as f:
            namelist = json.load(f)
        self.set_parameters(namelist)

    def set_parameters(self, namelist):
        avail = {}
        doc = {}
        for d in namelist.keys():
            dd = namelist[d]
            for name in dd.keys():
                val = dd[name]['default']
                # print(name, val)
                setattr(self, name, val)
                if 'avail' in dd[name]:
                    avail[name] = dd[name]['avail']
                if 'doc' in dd[name]:
                    doc[name] = dd[name]['doc']
        self.avail = avail
        self.doc = doc

    def man(self, name):
        if name in self.doc:
            helpstr = self.doc[name]
            if name in self.avail:
                availstr = ', '.join([str(l) for l in self.avail[name]])
                helpstr += ' / available values = ['+availstr+']'
        else:
            helpstr = 'no manual for this parameter'
        print('manual for %s : %s' % (name, helpstr))

    def manall(self):
        ps = self.listall()
        for p in ps:
            self.man(p)

    def checkall(self):
        for p, avail in self.avail.items():
            if getattr(self, p) in avail:
                # the parameter 'p' is well set
                pass
            else:
                msg = 'parameter "%s" should in ' % p
                msg += str(avail)
                raise ValueError(msg)

    def listall(self):
        """ return the list of all the parameters"""
        ps = [d for d in self.__dict__ if not(d in ['avail', 'doc'])]
        return ps

    def copy(self, obj, list_param):
        """ copy attributes listed in list_param to obj

        On output it returns missing attributes
        """
        missing = []
        for k in list_param:
            if hasattr(self, k):
                setattr(obj, k, getattr(self, k))
            else:
                missing.append(k)
        return missing


if __name__ == "__main__":
    param = Namelist()
    print('liste of parameters')
    print(param.listall())

    # to have the documentation on one particular parameter
    param.man('beta')

    # to get the documentation on all the parameters
    param.manall()

    # to check that all parameters that should a value taken from a list
    # have an acceptable value
    param.checkall()
