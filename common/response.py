def response_data(success, data=None):
    res = {'success': success}

    if success and isinstance(data, dict):
        # 단수
        res['data'] = data
    elif success:
        # 복수
        res['total_count'] = len(data)
        res['data'] = data
    else:
        # 에러
        res['error'] = data
    return res
