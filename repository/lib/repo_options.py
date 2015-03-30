#-*- encoding:utf-8 -*-
import os
import commands
from git import *

class RepoOptions(object):
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)
        self.git = self.repo.git

    def ls_tree(self, revision='', file_path=''):
        result = []
        if file_path == '':
            file_list = self.git.execute(['git', 'ls-tree', revision])
            file_list = [tmp.split('\t') for tmp in file_list.split('\n') if tmp]

            for file_info in file_list:
                record = {}
                tmp = file_info[0].split(' ')
                record['name'] = file_info[1]
                record['type'] = tmp[1]
                record['object_id'] = tmp[2]
                record['path'] = os.path.join(file_path, record['name'])
                log_info = self.file_log(revision, record['name']).split('$$')
                if log_info:
                    print log_info
                    record['committed_date'] = log_info[0]
                    record['message'] = log_info[1]
                else:
                    record['committed_date'] = ''
                    record['message'] = ''
                result.append(record)
        else:
            current_path = os.getcwd()
            os.chdir(self.repo_path)
            file_list = [tmp for tmp in commands.getoutput('git show %s:%s' %
                    (revision,file_path)).split('\n') if tmp][1:]
            for file_info in file_list:
                print "file_name:%s" % file_info
                record = {}
                if file_info.endswith('/'):
                    record['type'] = 'tree'
                    file_info = file_info[:-1]
                else:
                    record['type'] = 'blob'
                print file_info
                record['name'] = file_info
                record['path'] = os.path.join(file_path, record['name'])
                log_info = self.file_log(revision, record['path']).split('$$')
                print 'path:%s' % record['path']
                if log_info:
                    print log_info
                    record['committed_date'] = log_info[0]
                    record['message'] = log_info[1]
                else:
                    record['committed_date'] = ''
                    record['message'] = ''
                result.append(record)
            os.chdir(current_path)
        return result

    def file_log(self, revision='', file_name='', format='%cr$$%s'):
        return self.git.execute(['git', 'log', '--pretty=format:%s' % format, revision, '--', file_name])

    def show_file_content(self, revision='', file_path=''):
        """显示指定版本的文件内容"""

        return self.git.execute(['git', 'show', "%s:%s" % (revision, file_path)])