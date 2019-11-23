from datetime import datetime

#todo: REF: уточнить какой Exeption нужно ловить в этих декораторах. Пока он слишком общий.


def datetime_formatter_method_decorator(datetime_format_string="%Y-%m-%d"):
    def internal_function(function):
        def wrapper(*args, **kwargs):
            try:
                return datetime.strptime(function(*args, **kwargs), datetime_format_string)
            except Exception:
                return datetime.now()
        return wrapper
    return internal_function


def datetime_formatter_api_json_error_decorator(function):
    def internal_function(*args, **kwargs):
        res = function(*args, **kwargs)
        try:
            return datetime.strptime(res, "%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            return datetime.now()

    return internal_function


def aviasales_api_json_error_decorator(function):
    def internal_function(*args, **kwargs):
        res = function(*args, **kwargs)
        if isinstance(res, dict):
            if 'errors' in res.keys() and len(res['errors']) > 0:
                raise Exception('Data error occurred: %s ' % res['errors'])
        else:
            return res
    return internal_function