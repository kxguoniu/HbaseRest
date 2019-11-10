#-*- coding:utf-8 -*-
from HbaseRest.utils import _b64encode, _b64decode, CompareOp, Comparable, Operator
from collections import OrderedDict

__all__ = ["Filter"]

class Filter(object):
    def _filter(self, filter_type, value, op, c_type):
        comparator = self._buildComparator(value, c_type)
        self._CheckOp(op)
        data = OrderedDict([
            ("type", filter_type),
            ("op", op),
            ("comparator", comparator)
        ])
        return data

    def _buildComparator(self, value, c_type):
        self._CheckCtype(c_type)
        value = _b64encode(value)
        return OrderedDict([
            ("type", c_type),
            ("value", value)
        ])

    def _CheckOp(self, op):
        if op not in CompareOp:
            raise ValueError("%s not in %s" % (op, list(CompareOp)))

    def _CheckCtype(self, ctype):
        if ctype not in Comparable:
            raise ValueError("%s not in %s" % (ctype, list(Comparable)))

    def _CheckFilterListType(self, ftype):
        if ftype not in Operator:
            raise ValueError("%s not in %s" % (ftype, list(Operator)))

    def ColumnCountGetFilter(self, limit):
        # 返回前limit条数据
        return OrderedDict([("type", "ColumnCountGetFilter"), ("limit", limit)])

    def ColumnPaginationFilter(self, limit, offset):
        # 从offset行计算返回limit行数据
        return OrderedDict([
            ("type", "ColumnPaginationFilter"),
            ("limit", limit),
            ("offset", offset)
        ])

    def ColumnPrefixFilter(self, qualifier):
        # 返回指定列前缀匹配的行数据
        qualifier = _b64encode(qualifier)
        return OrderedDict([
            ("type", "ColumnPrefixFilter"),
            ("qualifier", qualifier)
        ])

    def ColumnRangeFilter(self, mincolumn, maxcolumn, flag1=True, flag2=True):
        # 返回列值在范围之间的行数据
        mincolumn = _b64encode(mincolumn)
        maxcolumn = _b64encode(maxcolumn)
        return OrderedDict([
            ("type", "ColumnRangeFilter"),
            ("minColumn", mincolumn),
            ("minColumnInclusive", flag1),
            ("maxColumn", maxcolumn),
            ("maxColumnInclusive", flag2)
        ])

    def ColumnValueFilter(self, family, qualifier, value, op="EQUAL", c_type="BinaryComparator"):
        # 匹配列值的数据
        comparator = self._buildComparator(value, c_type)
        family = _b64encode(family)
        qualifier = _b64encode(qualifier)
        self._CheckOp(op)
        return OrderedDict([
            ("type", "ColumnValueFilter"),
            ("op", op),
            ("family", family),
            ("qualifier", qualifier),
            ("comparator", comparator)
        ])

    def DependentColumnFilter(self):
        pass

    def FamilyFilter(self, family, op="EQUAL", c_type="BinaryComparator"):
        return self._filter("FamilyFilter", family, op, c_type)

    def QualifierFilter(self, qualifier, op="EQUAL", c_type="BinaryComparator"):
        return self._filter("QualifierFilter", qualifier, op, c_type)

    def RowFilter(self, row_key, op="EQUAL", c_type="BinaryComparator"):
        return self._filter("RowFilter", row_key, op, c_type)

    def ValueFilter(self, value, op="EQUAL", c_type="BinaryComparator"):
        return self._filter("ValueFilter", value, op, c_type)

    def FirstKeyOnlyFilter(self):
        return OrderedDict([("type", "FirstKeyOnlyFilter")])

    def FilterList(self, op="MUST_PASS_ALL"):
        self._CheckFilterListType(op)
        return OrderedDict([
            ("type", "FilterList"),
            ("op", op),
            ("filters", [])
        ])

    def FuzzyRowFilter(self, lists):
        #("????_999", "11110000")
        pass

    def InclusiveStopFilter(self, stop_row):
        # 指定停止行
        pass

    def KeyOnlyFilter(self):
        # 获取所有的键,不取值
        return OrderedDict([("type", "KeyOnlyFilter")])

    def MultipleColumnPrefixFilter(self, prefixes):
        # 返回指定前缀列表的列
        pass

    def MultiRowRangeFilter(self, row_list):
        # 扫描行键范围,非常迅速
        pass

    def PageFilter(self, size):
        # 指定大小的行数
        return OrderedDict([
            ("type", "PageFilter"),
            ("value", size)
        ])

    def PrefixFilter(self, pre_row):
        # 返回行前缀的数据
        pre_row = _b64encode(pre_row)
        return OrderedDict([
            ("type", "PrefixFilter"),
            ("value", pre_row)
        ])

    def RandomRowFilter(self):
        pass

    def SingleColumnValueFilter(self, family, qualifier, value, op="EQUAL", c_type="BinaryComparator", miss=False, late=True):
        # 匹配指定 家族和限定词的值, miss 找不到列防止发送整个行, late,默认匹配最后一个版本的值
        comparator = _buildComparator(value, c_type)
        self._CheckOp(op)
        family = _b64encode(family)
        qualifier = _b64encode(qualifier)
        return OrderedDict([
            ("type", "SingleColumnValueFilter"),
            ("op", op),
            ("family", family),
            ("qualifier", qualifier),
            ("latestVersion", late),
            ("ifMissing", miss),
            ("comparator", comparator)
        ])

    def SingleColumnValueExcludeFilter(self, family, qualifier, value, op="EQUAL", c_type="BinaryComparator", miss=False, late=True):
        # 返回数据不包含筛选的列
        comparator = _buildComparator(value, c_type)
        self._CheckOp(op)
        family = _b64encode(family)
        qualifier = _b64encode(qualifier)
        return OrderedDict([
            ("type", "SingleColumnValueExcludeFilter"),
            ("op", op),
            ("family", family),
            ("qualifier", qualifier),
            ("latestVersion", late),
            ("ifMissing", miss),
            ("comparator", comparator)
        ])

    def SkipFilter(self):
        # 筛选数据
        return OrderedDict([("type", "SkipFilter"), ("filters", [])])