from rest_framework.utils.serializer_helpers import ReturnList


def response_data(success, data=None):
    res = {}

    if success and (isinstance(data, ReturnList) or isinstance(data, list)):
        # 복수
        res['success'] = 'YES'
        res['total_count'] = len(data)
        res['data'] = data
    elif success:
        # 단수
        res['success'] = 'YES'
        res['data'] = data
    else:
        # 에러
        res['success'] = 'NO'
        res['msg'] = str(data)
    return res
