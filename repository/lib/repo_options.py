#-*- encoding:utf-8 -*-
import os
import commands
from git import *

class MyCommitObj(object):
    def __init__(self, commit_id='', author_name='', author_email='', authored_date='',
        committer_name='', committer_email='', committered_date='', title='', message=''):
        self.commit_id = commit_id
        self.author_name = author_name
        self.author_email = author_email
        self.authored_date = authored_date[:10]
        self.committer_name = committer_name
        self.committer_email = committer_email
        self.committered_date = committered_date[:10]
        self.title = title
        self.message = message


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

    def reference_commit_count(self, revision=''):
        """统计reference上commit的总数"""

        return len([tmp for tmp in self.git.execute(['git', 'log',
            '--pretty=format:%h', revision]).split('\n') if tmp])

    def commits(self, revision=''):
        """revision commit history"""

        format_str='%h<-#->%an<-#->%ae<-#->%ad<-#->%cn<-#->%ce<-#->%cd<-#->%s<-#->%b'
        status, history = commands.getstatusoutput('git --git-dir=%s log --date=iso --pretty=format:"%s" %s'
            % ( self.repo_path, format_str, revision))
        if status:
            return False, []
        else:
            commit_list = []
            history = history.split('\n')
            for commit_line in history:
                if commit_line:
                    commit_line = commit_line.split('<-#->')
                    if len(commit_line) == 9:
                        commit = MyCommitObj(commit_line[0], commit_line[1], commit_line[2], commit_line[3], commit_line[4]
                        , commit_line[5], commit_line[6], commit_line[7], commit_line[8])
                    else:
                        commit = MyCommitObj(message=''.join(commit_line))
                    commit_list.append(commit)

            return True, commit_list

    def show_object(self, object_str=''):
        """show git object info"""

        return self.git.execute(['git', 'show', object_str])

