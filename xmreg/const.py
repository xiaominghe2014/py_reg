#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@version: ??
@author: xiaoming
@license: MIT Licence 
@contact: xiaominghe2014@gmail.com
@site: 
@software: PyCharm
@file: const.py
@time: 2017/12/19 下午3:07

"""
import sys


class Const:
    class ConstError(TypeError):
        pass

    def __init__(self):
        pass

    def __setattr__(self, key, value):
        if self.__dict__.has_key(key):
            raise self.ConstError, 'can\'t rebind const (%s)' % key
        self.__dict__[key] = value

    @staticmethod
    def other(other):
        return '([^{}])'.format(other)

    @staticmethod
    def repeat_n(s, n):
        return '((%s){%s})' % (s, n)

    @staticmethod
    def repeat_n_m(s, n, m):
        return '((%s){%s,%s})' % (s, n, m)

    @staticmethod
    def find(s):
        return '({})'.format(s)

    @staticmethod
    def maybe(s):
        return '(({})?)'.format(s)

    @staticmethod
    def from_to(begin, end):
        return '([{}-{}])'.format(begin, end)

    @staticmethod
    def a_or_b(a, b):
        return '({a}|{b})'.format(a=a, b=b)

    @staticmethod
    def any_char():
        return '(.)'

    @staticmethod
    def string_most(s):
        return '(({})*)'.format(s)

    @staticmethod
    def string_1_or_more(s):
        return '(({})+)'.format(s)

    @staticmethod
    def string_0_or_1(s):
        return '(({})?)'.format(s)


sys.modules[__name__] = Const()

