#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@version: ??
@author: xiaoming
@license: MIT Licence 
@contact: xiaominghe2014@gmail.com
@site: 
@software: PyCharm
@file: base_define.py
@time: 2017/12/19 下午12:11

"""
import const as xreg

xreg.repeat_0_or_more = '*'
xreg.repeat_1_or_more = '+'
xreg.repeat_0_or_1 = '?'
xreg.char_any = '.'
xreg.begin = '^'
xreg.end = '$'

# eg. [1-9]
xreg.r_from = '['
xreg.r_id = '-'
xreg.r_to = ']'

xreg.save_begin = '('
xreg.save_end = ')'


class RegSign:

    def __init__(self, reg=''):
        self.version = '0.0.0'
        self.reg = reg

    def other(self, other):
        self.reg = '{}{}'.format(self.reg, xreg.other(other))
        return self

    def repeat_n(self, s, n):
        self.reg = '{}{}'.format(self.reg, xreg.repeat_n(s, n))
        return self

    def repeat_n_to_m(self, s, n, m):
        self.reg = '{}{}'.format(self.reg, xreg.repeat_n_m(s, n, m))
        return self

    def find(self, s):
        self.reg = '{}{}'.format(self.reg, xreg.find(s))
        return self

    def maybe(self, s):
        self.reg = '{}{}'.format(self.reg, xreg.maybe(s))
        return self

    def from_to(self, begin, end):
        self.reg = '{}{}'.format(self.reg, xreg.from_to(begin, end))
        return self

