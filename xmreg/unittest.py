#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@version: ??
@author: xiaoming
@license: MIT Licence 
@contact: xiaominghe2014@gmail.com
@site: 
@software: PyCharm
@file: unittest.py
@time: 2017/12/21 下午2:50

"""
# import reg_cpu
from reg_cpu import RegexCpu as Regex
from reg_cpu import RegexOption as Option


def print_obj_attr(obj):
    for key in obj.__dict__:
        print('%s:%s' % (key, obj.__dict__[key]))


def main():
    search_src = 'x001y234&*80@019c)56>78900121.3456700-89":'
    search_txt = '0'
    res_find = Regex().search(search_src, search_txt, Option.find, repeat_times=2)
    res_other = Regex().search(search_src, search_txt, Option.other, repeat_times=2)
    print(res_find, res_other)

    for i in xrange(len(res_find)):
        print(res_find[i][0], res_find[i][1])
        print(search_src[res_find[i][0]:res_find[i][1]])
    for i in xrange(len(res_other)):
        print(res_other[i][0], res_other[i][1])
        print(search_src[res_other[i][0]:res_other[i][1]])
    print('\d' == '\\d')
    reg = Regex()
    reg_str = ['[A-Za-z0-9_]', 'abcd{3}', 'abcd{3,}', 'abcd{3,10}', '[^0-9]', '(\)?', '(123)*', '(&%)+', '(1|22|23|4)']
    for i in reg_str:
        print_obj_attr(reg.get_regex_atom(i))
    res = reg.regex_atom_add(reg.get_regex_atom('\d'), reg.get_regex_atom('x{3}'))
    for atom in res:
        print_obj_attr(atom)


if __name__ == '__main__':
    main()



