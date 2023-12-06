def success_response(message=None, data=None, count=None):
    result = dict(success=True)
    result['message'] = message or ''
    result['data'] = data or {}
    if count is not None:
        result['count'] = count
    return result


def failure_response(message=None, data=None):
    result = dict(success=False)
    result['message'] = message or ''
    result['data'] = data or {}
    return result