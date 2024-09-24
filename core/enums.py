import enum


class FormatType(enum.Enum):
    """
    FormatType enum
    """
    CURRENCY = 'currency'
    DATE = 'date'
    DATETIME = 'datetime'
    DECIMAL = 'decimal'
    TIME = 'time'
    INTEGER = 'integer'
    LINK = 'link'
    PERCENT = 'percent'
    BOOLEAN = 'boolean'
