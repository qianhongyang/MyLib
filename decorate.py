#coding=utf-8


def decorate(func):
    def wrap(*arg,**kw):
        print "you are right!"
        func(*arg,**kw)
    return wrap

def decorate2(func):
    def wrap(*args,**kw):
        a=1
        func(*args,**kw)
        print "you are right two"
    return wrap

@decorate2
def do(a,b,c):
    print "dosomething！"
    print a+b+c



class TestDecorate(object):
    def __init__(self,a):
        self.a=a
        self._s=a
    def __call__(self, *args, **kwargs):
        print "The begin"
        c=3
        self.a()
        print "The end"

@TestDecorate
def ok():
    print "just do it !"

ok()