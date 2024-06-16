import json


class ComVo:
    def __str__(self):
        json_str = json.dumps(self.__dict__, ensure_ascii=False,
                              default=lambda o: json_serial_default_fun(o))
        return json_str

    def __repr__(self):
        return self.__str__()


def json_serial_default_fun(o):
    """
    json序列化default方法
    如果元素有__dict__属性，即对象, 返回对象的__dict__方法；
    如果元素是set, 则转为list;
    否则，直接返回对象本身。
    :param o: 元素
    :return: 返回
    """
    if isinstance(o, set):
        return list(o)
    if hasattr(o, '__dict__'):
        return o.__dict__
    else:
        return o