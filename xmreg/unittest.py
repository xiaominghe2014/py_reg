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
from reg_cpu import RegexCpu as Regex
from reg_cpu import RegexOption as Option


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


if __name__ == '__main__':
    main()



