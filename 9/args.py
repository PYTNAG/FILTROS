class Arguments:
    def __init__(self):
        self.args = {}
        self.associations = []

    def parse(self, argv: list[str]) -> None:
        last_key = ""
        for arg in argv:
            if arg.startswith(("-", "--")):
                self.args[arg] = True
                last_key = arg
            else:
                if type(self.args[last_key]) != list:
                    self.args[last_key] = []
                self.args[last_key].append(arg)

    def add_association(self, synonyms: tuple[str]):
        self.associations.append(set(synonyms))
    
    def get_value(self, arg_name: str) -> list[str]:
        for a in self.associations:
            if arg_name in a:
                arg_name = a
                break
        
        if type(arg_name) == str:
            arg_name = [arg_name]

        u = set(arg_name).intersection(self.args)
        
        return self.args[u.pop()] if u != set() else None