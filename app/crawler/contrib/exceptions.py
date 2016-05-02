# -*- coding: utf-8 -*-
class SchemaValidationException(Exception):
    pass


class DupeValidationException(SchemaValidationException):
    pass
