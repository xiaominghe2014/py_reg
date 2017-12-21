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


def enum(**enums):
    return type('Enum', (), enums)


const.MaxBranch = 100
const.MaxAtom = 100
const.RegexKey = '^$().[-]*+?|\\WwSsdbfnrtv'
RegexOption = enum(
    find=0,
    other=1
)


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

####################################
#
# CPU  end
#
#####################################


