import json


class ComVo:
    def __str__(self):
        json_str = json.dumps(self.__dict__, ensure_ascii=False,
                              default=lambda o: o.__dict__ if hasattr(o, '__dict__') else o)
        return json_str

    def __repr__(self):
        return self.__str__()
