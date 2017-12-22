#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@version: ??
@author: xiaoming
@license: MIT Licence 
@contact: xiaominghe2014@gmail.com
@site: 
@software: PyCharm
@file: reg_cpu.py
@time: 2017/12/19 下午5:45

"""

import const as const

const.repeatAddMax = 1024


def enum(**enums):
    return type('Enum', (), enums)


def from_to(char_from, char_to):
    res = list()
    for x in xrange(ord(char_to)-ord(char_from)+1):
        res.append([chr(x+ord(char_from))])
    return res


def get_char_index(arg_str, char):
    res = list()
    for x in xrange(len(arg_str)):
        if char == arg_str[x]:
            res.append(x)
    return res


def repeat_str(arg_str):
    len_str = len(arg_str)
    if len_str < 4:
        return [arg_str, 1]
    if '}' == arg_str[len_str - 1] and '\\' != arg_str[len_str - 2]:
        for i in xrange(len_str):
            idx = len_str-i-1
            if idx and '{' == arg_str[idx] and '\\' != arg_str[idx-1]:
                new_str = arg_str[idx+1:len_str-1]
                comma_index = get_char_index(new_str, ',')
                comma_total = len(comma_index)
                if not comma_total:
                    repeat_times = int(new_str)
                    return [arg_str[:idx]*repeat_times, 1]
                elif 1 == comma_total:
                    repeat_min = int(new_str[:comma_index[0]])
                    repeat_max = (comma_index[0] < len(new_str)-1 and
                                  int(new_str[comma_index[0]+1:len(new_str)]) or
                                  const.repeatAddMax+repeat_min)
                    return [arg_str[:idx], repeat_min, repeat_max]
    return [arg_str, 1]


def char_set(arg_str):
    if '[' == arg_str[0] and ']' == arg_str[len(arg_str)-1]:
        index_list = list()
        res = list()
        for i in xrange(len(arg_str)):
            if 0 < i - 1:
                if '-' == arg_str[i] and i + 1 < len(arg_str) - 1:
                    index_list.append(i)
                elif i + 1 < len(arg_str) and '-' != arg_str[i-1] and '-' != arg_str[i+1]:
                    res.append([arg_str[i]])
        for j in xrange(len(index_list)):
            res.extend(from_to(arg_str[index_list[j]-1], arg_str[index_list[j]+1]))
        return res
    else:
        return list()


const.MaxBranch = 100
const.MaxAtom = 100
const.RegexKey = '^$().[-]*+?|\\WwSsdbfnrtv'
const.number = char_set('[0-9]')
const.blank = '\f,\n,\r,\t,\v'.split(',')
const.w = char_set('[A-Za-z0-9_]')
const.reg_range = ['\d', '\D', '\s', '\S', '\w', '\W']
RegexOption = enum(
    find=0,
    other=1,
    any=2
)


####################################
#
# Regex  Atom
#
#####################################

class RegexAtom:
    def __init__(self):
        self.regex = ''
        self.option = 0
        # strings is a charset(list) ,
        #  0 is string, 1 is min repeat times, 2 is max repeat times
        self.strings = list()


####################################
#
# CPU  begin
#
#####################################

class RegexCpu:

    def __init__(self):
        self.version = '0.0.0'

    def search(self, txt_src, txt_target, reg_option=RegexOption.find, repeat_times=1):
        txt_target = txt_target*repeat_times
        if reg_option == RegexOption.find:
            return self.find(txt_src, txt_target)
        if reg_option == RegexOption.other:
            return self.other(txt_src, txt_target)
        return list()

    '''
    @:brief 从给定的字符中寻找目标字符 暂用kmp算法，bm算法还没有校验
    @:param txt_src 源字符 txt_target 目标字符
    @:return list  txt_src的匹配位置数组
    '''
    def find(self, txt_src, txt_target):
        res = list()
        len_src = len(txt_src)
        len_target = len(txt_target)
        if len_src >= len_target:
            search_pos = 0
            move_small = self.get_kmp_len(txt_target) or 1
            move_pos = move_small
            while search_pos+len_target <= len_src:
                if txt_target == txt_src[search_pos:search_pos+len_target]:
                    res.append([search_pos, search_pos+len_target])
                search_pos = search_pos + move_pos
        return res

    def other(self, txt_src, txt_target):
        res = list()
        len_src = len(txt_src)
        len_target = len(txt_target)
        if len_src >= len_target:
            search_pos = 0
            start_pos = 0
            move_small = self.get_kmp_len(txt_target) or 1
            move_pos = move_small
            while search_pos+len_target <= len_src:
                if txt_target == txt_src[search_pos:search_pos+len_target]:
                    if start_pos < search_pos:
                        res.append([start_pos, search_pos])
                    start_pos = search_pos+len_target
                search_pos = search_pos + move_pos
            if 0 < start_pos < len_src:
                res.append([start_pos, len_src])
        if not len(res) and len_src:
            res.append([0, len_src])
        return res

    @staticmethod
    def get_kmp_len(txt_target):
        res = 0
        len_target = len(txt_target)
        if len_target > 1:
            next_index = 1
            while next_index < len_target:
                if txt_target[:next_index] == txt_target[-next_index:]:
                    res = next_index
                next_index = next_index+1
        return res

    def get_bm_len(self, txt_src, txt_target):
        res = 0
        len_src = len(txt_src)
        len_target = len(txt_target)
        if len_src >= len_target:
            if txt_src[:len_target-1] != txt_target[:len_target-1]:
                return self.get_bad_len(txt_target, txt_src[:len_target-1])
            else:
                return self.get_good_len(txt_src, txt_target)
        return res

    @staticmethod
    def get_bad_len(txt_target, bad_char):
        len_target = len(txt_target)
        for i in xrange(len_target):
            if txt_target[len_target-i-1] == bad_char:
                return i
        return len_target

    def get_good_len(self, txt_src, txt_target):
        len_target = len(txt_target)
        search_idx = 1
        while search_idx < len_target:
            if txt_src[len_target-search_idx:len_target] == \
                    txt_target[len_target-search_idx:len_target]:
                search_idx = search_idx+1
            else:
                break
        good_tail = txt_target[len_target-search_idx+1:len_target]
        len_tail = search_idx-1
        len_bad = self.get_bad_len(txt_target[:len_target-len_tail], txt_src[len_target-len_tail-1])
        head_idx = 0
        while head_idx < len_tail:
            if txt_target[:len_target-head_idx] != good_tail[head_idx:len_tail]:
                head_idx = head_idx+1
            else:
                break
        return max(len_target-head_idx-1, len_bad)

    def match(self, txt_src, txt_target, reg_option=RegexOption.find, repeat_times=1):
        txt_target = txt_target * repeat_times
        if reg_option == RegexOption.find:
            return len(self.find(txt_src, txt_target))
        if reg_option == RegexOption.other:
            return len(self.other(txt_src, txt_target))
        return 0

    @staticmethod
    def reg_range_map(reg_char):
        reg_list = [
            {
                '\d': const.number,
                'option': RegexOption.find
            },
            {
                '\D': const.number,
                'option': RegexOption.other
            },
            {
                '\s': const.blank,
                'option': RegexOption.find
            },
            {
                '\S': const.blank,
                'option': RegexOption.other
            },
            {
                '\w': const.w,
                'option': RegexOption.find
            },
            {
                '\W': const.w,
                'option': RegexOption.other
            },
        ]
        res = RegexAtom()
        for i in xrange(len(reg_list)):
            if reg_char in reg_list[i].keys():
                res.option = reg_list[i]['option']
                res.strings = reg_list[i][reg_char]
                return res
        return res

    def get_regex_atom(self, reg):
        res = RegexAtom()
        res.regex = reg
        if len(reg) < 2:
            res.strings.append([reg])
        elif reg[0:2] in const.reg_range:
            return self.reg_range_map(reg[1])
        elif '}' == reg[len(reg)-1] and '\\' != reg[len(reg)-2]:
            c_reg = self.check_other(reg)
            res.option = c_reg and RegexOption.other or RegexOption.find
            repeat_list = repeat_str(c_reg or reg)
            if 2 == len(repeat_list):
                res.strings.append([repeat_list[0]])
            if 3 == len(repeat_list):
                    res.strings.append([repeat_list[0], repeat_list[1], repeat_list[2]])
            return res
        elif ']' == reg[len(reg)-1] and '\\' != reg[len(reg)-2]:
            c_reg = self.check_other(reg)
            res.option = c_reg and RegexOption.other or RegexOption.find
            res.strings = char_set(c_reg or reg)
            return res
        elif '*' == reg[len(reg)-1] and ')' == reg[len(reg)-2] and ')' != reg[0]:
            res.strings.append([reg[1:-2], 0, const.repeatAddMax])
        elif '+' == reg[len(reg)-1] and ')' == reg[len(reg)-2] and ')' != reg[0]:
            res.strings.append([reg[1:-2], 1, const.repeatAddMax])
        elif '?' == reg[len(reg)-1] and ')' == reg[len(reg)-2] and ')' != reg[0]:
            res.strings.append([reg[1:-2], 0, 1])
        elif ')' == reg[len(reg)-1] and '(' == reg[0]:
            res.strings.append(self.char_set_or(reg[1:-1]))
        return res

    @staticmethod
    def check_other(reg):
        if '^' == reg[1]:
            return reg[0]+reg[2:]
        return ''

    @staticmethod
    def char_set_or(arg_str):
        dem = '|'
        res = arg_str.split(dem)
        start_index = 0
        while start_index < len(res)-1:
            s_len = len(res[start_index])
            if '\\' == res[start_index][s_len-1]:
                res[start_index+1] = res[start_index]+res[start_index+1]
                res.remove(res[start_index])
            else:
                start_index += 1
        result = list()
        for value in res:
            result.append([value])
        if not len(result):
            result.append([arg_str])
        return result

####################################
#
# CPU  end
#
#####################################


