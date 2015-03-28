#-*- encoding:utf-8 -*-
import time


def get_current_time(fromat_str='%Y-%m-%d %H:%M:%S'):
    """获取格式的时间"""

    return time.strftime(fromat_str)


def session_context(request):
    return {'session': request.session}

if __name__ == '__main__':
    print get_current_time()