def response_data(success, data=None, now_page=None, max_page=None):
    res = {'success': success}

    if success and (isinstance(data, dict) or data is None):
        # 단수
        res['data'] = data
    elif success:
        # 복수
        if now_page is not None:
            res['max_page'] = max_page
            res['now_page'] = now_page
        res['total_count'] = len(data)
        res['data'] = data
    else:
        # 에러
        res['error'] = data
    return res
