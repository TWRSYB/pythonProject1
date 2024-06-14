import json


class ComVo:
    def __str__(self):
        json_str = json.dumps(self.__dict__, ensure_ascii=False,
                              default=lambda o: object_to_dict_or_self(o))
        return json_str

    def __repr__(self):
        return self.__str__()


def object_to_dict_or_self(o):
    """
    如果对象o有__dict__属性，则返回该属性（即对象的属性字典）；
    否则，直接返回对象本身。
    """
    if isinstance(o, set):
        return list(o)
    if hasattr(o, '__dict__'):
        return o.__dict__
    else:
        return o