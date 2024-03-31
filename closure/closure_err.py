import functools
import types


def counter(cls):
    obj_list = []

    # 被装饰后的就会变成一个函数，需要使用functools.wraps(cls)修正
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        new_obj = cls(*args, **kwargs)
        obj_list.append(new_obj)
        print("class:%s'object number is %d" % (cls.__name__, len(obj_list)))
        return new_obj
    return wrapper

@counter
class my_cls(object):
    STATIC_MEM = 'This is a static member of my_cls'
    def __init__(self, *args, **kwargs):
        print(self, args, kwargs)
        print(my_cls.STATIC_MEM)
print(my_cls.__name__ == 'wrapper' and type(my_cls) is types.FunctionType)
cls_obj = my_cls()