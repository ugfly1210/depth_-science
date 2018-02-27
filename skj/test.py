def Singleton(cls):
    _instance = {}
    def _Singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return _Singleton

@Singleton
class A:
    a = 1
    def __init__(self,x=0):
        self.x = x
a1 = A(2)
a2 = A(3)

print(id(a1))
print(id(a2))
print(a1.x)
print(a2.x)