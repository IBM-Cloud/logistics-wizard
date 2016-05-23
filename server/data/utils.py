"""
Module containing database utility methods and extensions for the Base model
class.
"""
import re

from sqlalchemy import text, bindparam
from sqlalchemy.orm.attributes import InstrumentedAttribute

# Pattern for search fields
_SEARCH_FIELD_RE = re.compile('([^=<>,\';]+)([=<>]{1,2})([^=<>,\';]+),?')


def parse_search_fields(search_string):
    """
    Takes a search string in format specified below and returns a list
    of search fields.

    :param search_string:  [field_name][operation][value]

     field_name  - Cannot contain =<>,'; characters
     operation   - Any of the following: =, <, <=, >, >=
     value       - Cannot contain =<>,'; characters

    :return:
    [{
        'name': 'field_name',
        'op': '=',
        'value': 'value'
    }, {
        ...
    }]
    """
    if search_string is None:
        search_string = ''
    return [{'name': x[0], 'op': x[1], 'value': x[2]}
            for x in re.findall(_SEARCH_FIELD_RE, search_string)]


def build_text_filter(model, field_list):
    """
    Build a list of SQLAlchemy filters for searching.

    :param model:       The SQLAlchemy model.
    :param field_list:  A list of fields of the same form as generated
                        by parse_search_fields.
    :return:            An array of text filters that can be passed to
                        SQLAlchemy queries.
    """
    filter_list = []
    for field in field_list:
        try:
            col_attr = model.__getattribute__(model, field['name'])
            if type(col_attr) is InstrumentedAttribute:
                stmt = text('{0}{1}:{2}'.format(field['name'],
                                                field['op'],
                                                field['name']))
                stmt = stmt.bindparams(bindparam(field['name'],
                                                 value=field['value']))
                filter_list.append(stmt)
            else:
                raise AttributeError()

        except AttributeError as e:
            raise AttributeError(
                    '{0} has no attribute {1}'.format(model.__name__,
                                                      field['name']))
    return filter_list


def search_property():
    """
    Returns a class method that will parse the appropriate search fields
    out of the input string and build a query with filters.
    """
    @classmethod
    def search(cls, search_string):
        fields = _parse_search_fields(search_string)
        filters = _build_text_filter(cls, fields)
        return cls.query.filter(*filters)
    return search
