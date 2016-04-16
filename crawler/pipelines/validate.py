# -*- coding: utf-8 -*-
from jsonschema import validate, ValidationError
from ..contrib.exceptions import SchemaValidationException


class ValidatePipeline(object):

    def process_item(self, item, spider):
        """ Validate item against validation schema. """
        spider.logger.info('Schema validation')
        # validate item against validation schema
        try:
            validate(dict(item), item.json_schema_validation)
        except ValidationError as e:
            message = 'Schema exception. Path {}, Validator {}, Message {}, Cause {}'.format(
                e.path,
                e.validator,
                e.message,
                e.cause
            )
            spider.logger.warning(message)
            spider.crawler.stats.inc_value('validation_exceptions')
            raise SchemaValidationException(e)
        return item
