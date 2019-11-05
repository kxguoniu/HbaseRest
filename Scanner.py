# -*- coding:utf-8 -*-
from utils import _b64encode, _b64decode, Operator
from xml.etree import ElementTree
from Filter import Filter
from uuid import uuid1
import json

def build_kwargs_data(**kwargs):
    return {args[0]:args[1] for args in kwargs.items() if args[1] is not None}

class Scanner(object):
    def __init__(self, start_row=None, end_row=None, batch=None, data=None, op=Operator.all):
        self.start_row = start_row
        self.end_row = end_row
        self.batch = batch
        self.filter = Filter()
        self.data = data if data else self.filter.FilterList(op)

    def export_xml(self):
        et = ElementTree
        xml = et.Element("Scanner")
        xml.set("id", str(uuid1()))
        if self.start_row: xml.set("startRow", _b64encode(self.start_row))
        if self.end_row: xml.set("endRow", _b64encode(self.end_row))
        if self.batch: xml.set("batch", str(self.batch))
        if self.data["filters"]:
            filters = et.SubElement(xml, "filter")
            filters.text = json.dumps(self.data)

        return et.tostring(xml).decode()

    def append(self, value):
        self.data["filters"].append(value)

    def extend(self, values):
        for value in values:
            self.append(value)

    def build_column_count_get_filter(self, limit):
        return self.filter.ColumnCountGetFilter(limit)

    def build_column_pagination_filter(self, limit, offset):
        return self.filter.ColumnPaginationFilter(limit, offset)

    def build_column_prefix_filter(self, qualifier):
        return self.filter.ColumnPrefixFilter(qualifier)

    def build_column_range_filter(self, min_column, max_column, flag1=True, flag2=True):
        return self.filter.ColumnRangeFilter(min_column, max_column, flag1, flag2)

    def build_column_value_filter(self, column, value, op=None, c_type=None):
        family, qualifier = column.split(":")
        if family and qualifier:
            kwargs = build_kwargs_data(op=op, c_type=c_type)
            return self.filter.ColumnValueFilter(family, qualifier, value, **kwargs)
        else:
            raise ValueError("column must be 'family:qualifier'")

    def build_single_column_value_filter(self, column, value, op=None, c_type=None, miss=None, late=None):
        family, qualifier = column.split(":")
        if family and qualifier:
            kwargs = build_kwargs_data(op=op, c_type=c_type, miss=miss, late=late)
            return self.filter.SingleColumnValueFilter(family, qualifier, value, **kwargs)
        else:
            raise ValueError("column must be 'family:qualifier'")

    def build_single_column_value_exclude_filter(self, column, value, op=None, c_type=None, miss=None, late=None):
        family, qualifier = column.split(":")
        if family and qualifier:
            kwargs = build_kwargs_data(op=op, c_type=c_type, miss=miss, late=late)
            return self.filter.SingleColumnValueExcludeFilter(family, qualifier, value, **kwargs)
        else:
            raise ValueError("column must be 'family:qualifier'")

    def build_row_filters(self, row_key, **kwargs):
        if isinstance(row_key, str):
            return self.filter.RowFilter(row_key, **kwargs)
        elif isinstance(row_key, list) and row_key:
            if all(isinstance(one, str) for one in row_key):
                filter_list = self.filter.FilterList(Operator.one)
                for row_one in row_key:
                    row_filter = self.filter.RowFilter(row_one, **kwargs)
                    filter_list["filters"].append(row_filter)
                return filter_list
            else:
                raise ValueError("row_key list must be str list")
        else:
            raise ValueError("row_key must be str or list")

    def _build_column_one(self, column, **kwargs):
        if ":" in column:
            family, qualifier = column.split(":", 1)
            if qualifier:
                filter_list = self.filter.FilterList()
                filter_list["filters"].append(self.filter.FamilyFilter(family, **kwargs))
                filter_list["filters"].append(self.filter.QualifierFilter(qualifier, **kwargs))
                return filter_list
            else:
                return self.filter.FamilyFilter(family, **kwargs)
        else:
            return self.filter.QualifierFilter(column, **kwargs)

    def build_column_filters(self, column, **kwargs):
        if isinstance(column, str):
            return self._build_column_one(column, **kwargs)
        elif isinstance(column, list) and column:
            if all(isinstance(one, str) for one in column):
                filter_list = self.filter.FilterList(Operator.one)
                for col_one in column:
                    filter_list["filters"].append(self._build_column_one(col_one, **kwargs))
                return filter_list
            else:
                raise ValueError("column list must be str list")
        else:
            raise ValueError("column must be str or list")

    def build_value_filters(self, value, **kwargs):
        if isinstance(value, str):
            return self.filter.ValueFilter(value, **kwargs)
        elif isinstance(value, list) and value:
            if all(isinstance(one, str) for one in value):
                filter_list = self.filter.FilterList(Operator.one)
                for val_one in value:
                    filter_list["filters"].append(self._build_column_one(val_one, **kwargs))
                return filter_list
            else:
                raise ValueError("value list must be str list")
        else:
            raise ValueError("value must be str or list")

    def build_skip_filters(self, skip_data):
        if isinstance(skip_data, tuple):
            if 2 <= len(skip_data) <= 6:
                if len(skip_data) >= 5:
                    return self.build_single_column_value_filter(*skip_data)
                else:
                    return self.build_column_value_filter(*skip_data)
            else:
                raise ValueError("skip_data length in [2,3,4,5,6]")
        elif isinstance(skip_data, list) and skip_data:
            if all(isinstance(one, tuple) and 2 <= len(one) <= 6 for one in skip_data):
                filter_list = self.filter.FilterList(Operator.one)
                for skip_one in skip_data:
                    if len(skip_data) >= 5:
                        filter_list["filters"].append(self.build_single_column_value_filter(*skip_data))
                    else:
                        filter_list["filters"].append(self.build_column_value_filter(*skip_data))
                return filter_list
            else:
                raise ValueError("skip_data list must be tuple list and tuple length in [2,3,4,5,6]")
        else:
            raise ValueError("skip_data must be tuple or list")

    def build_first_key_only_filter(self):
        return self.filter.FirstKeyOnlyFilter()

    def build_key_only_filter(self):
        return self.filter.KeyOnlyFilter()

    def build_page_filter(self, size):
        return self.filter.PageFilter(size)

    def build_prefix_filter(self, pre_row):
        return self.filter.PrefixFilter(pre_row)

    def build_skip_filter(self):
        return self.filter.SkipFilter()

def build_filter_xml(row_key, column, value, op=None, row_op=None, row_type=None,
                    col_op=None, col_type=None, val_op=None, val_type=None,
                    other_filter=None, skip_data=None, start_row=None,
                    end_row=None, batch=None, miss=False, late=True):
    scanner_filter = Scanner(start_row, end_row, batch, op=op) if op else Scanner(start_row, end_row, batch)
    if other_filter:
        scanner_filter.extend(other_filter)
    if row_key:
        kwargs = build_kwargs_data(op=row_op, c_type=row_type)
        row_filter = scanner_filter.build_row_filters(row_key, **kwargs)
        scanner_filter.append(row_filter)
    if column:
        kwargs = build_kwargs_data(op=col_op, c_type=col_type)
        column_filter = scanner_filter.build_column_filters(column, **kwargs)
        scanner_filter.append(column_filter)
    if value:
        kwargs = build_kwargs_data(op=val_op, c_type=val_type)
        value_filter = scanner_filter.build_value_filters(value, **kwargs)
        scanner_filter.append(value_filter)
    if skip_data:
        skip_filter = scanner_filter.build_skip_filters(skip_data)
        scanner_filter.append(skip_filter)

    filter_xml = scanner_filter.export_xml()
    return filter_xml

