import json
from dataclasses import is_dataclass

class SenfenicoJSONEncoder(json.JSONEncoder):
    def encode(self, o):
        if isinstance(o, dict):
            ret = ["{"]
            for k, v in o.items():
                if is_dataclass(v):
                    ret.append(f"\n{' ' * self.indent}{self.encode(k)}: {v},")
                else:
                    ret.append(f"\n{' ' * self.indent}{self.encode(k)}: {self.encode(v)},")
            ret.append(f"\n{' ' * (self.indent - 4)}{'}'}")
            return ''.join(ret)
        elif isinstance(o, list):
            ret = ["["]
            for i, e in enumerate(o):
                if is_dataclass(e):
                    ret.append(f"{e}")
                else:
                    ret.append(f"\n{' ' * self.indent}{self.encode(e)}")
                if i < len(o) - 1:
                    ret.append(",")
            ret.append(f"\n{' ' * (self.indent)}]")
            return ''.join(ret)
        else:
            return super().encode(o)

