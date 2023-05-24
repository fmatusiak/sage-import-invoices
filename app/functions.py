import pandas


def isNullOrEmpty(value):
    return not value or isNan(value)


def isNan(value):
    try:
        return pandas.isna(float(value))
    except ValueError:
        return False
