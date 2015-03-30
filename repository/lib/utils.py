#-*- encoding:utf-8 -*-
import os.path

#path turn to html href
def path_to_url(file_path, href=''):
    if file_path:
        file_path = '/'+file_path
        path_list = [tmp for tmp in file_path.split('/') if tmp]
        parent_path = ''
        result = []
        result.append('<a href="%s&file_path=%s">%s</a>' % (href, '', '#'))
        for path in path_list:
            parent_path = os.path.join(parent_path, path)
            result.append('<a href="%s&file_path=%s">%s</a>' % (href, parent_path, path))

        return '/'.join(result)
    else:
        return '<a href="%s&file_path=%s">%s</a>' % (href, '', '/')