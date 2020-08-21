# -*- coding:utf-8 -*-
from Scanner import build_filter_xml, Scanner
from utils import Comparable, CompareOp, Operator
import json

def decode_xml(data):
    data = data.split(">", 2)[-1].split("<")[0]
    print(json.dumps(json.loads(data), indent=4), end="\n\n\n")


def build(*args, **kwargs):
    decode_xml(build_filter_xml(*args, **kwargs))



args1 = ("kaixin", "family:qualifier", "")
args2 = (["kaixin", "kaixin"], "", "")
args3 = ("", "family:qualifier", "")
args4 = ("", "family:", "")
args5 = ("", "qualifier", "")
args6 = ("", "", "")

skip_data = None
skip_data1 = ("family:qualifier", "value", CompareOp.gt, Comparable.pre)
skip_data2 = (["value", "value"], "family:qualifier", "eq")
skip_data3 = ("value", "family:", "eq")

scan_filter = Scanner()
other_filter = scan_filter.

build(*args1, skip_data=skip_data1)