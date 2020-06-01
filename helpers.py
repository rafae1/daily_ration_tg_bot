from eating import Eating


def format_field(field_name, value):
    if field_name == "eating":
        return Eating.verbose(value)
    else:
        return value
