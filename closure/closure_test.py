


def my_func(*args):
    fs = []
    for i in range(3):
        # 当不使用关键字参数时，i的生命周期和闭包一样，所以结果全是4
        def func(_i=i):
            return _i * _i
        fs.append(func)
    return fs


if __name__ == '__main__':
    fs1, fs2, fs3 = my_func()
    print(fs1())
    print(fs2())
    print(fs3())
