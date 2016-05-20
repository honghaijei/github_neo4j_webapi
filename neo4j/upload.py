import utils
import json
from utils import get_streak
import openhub_project
import openhub_project_news
import time
from people_get import get_contributor
from people_merge import mess
from neo4j.models import *


def upload(data):
    projects = None
    project_news = None
    repositories = [data['repository']]
    releases = data['releases']
    issues = data['issues']
    contributors = data['contributors']
    commits = data['commits']
    commit_files = data['commit_files']
    trees = data['trees']
    repo_name = repositories[0]['repositoryName']
    for i in ProjectMapper.objects.all():
        if i.github == repositories[0]['htmlUrl']:
            repo_name = i.openhub.split('/')[-1]
    print("repo_name: " + repo_name)
    ret, repo_id = utils.get_node('repository_index', 'repository_id', repo_name)
    if ret != None:
        raise KeyError("duplicate")
    retry = 1000
    while retry != 0:
        try:
            if projects is None:
                projects = [openhub_project.get_project(repo_name)]
            if project_news is None:
                project_news = [openhub_project_news.get_project_news(repo_name)]
            break
        except:
            retry -= 1
            time.sleep(1)
            pass
    if projects is None:
        raise KeyError("Not found.")
    if project_news is None:
        raise KeyError("Not found.")
    openhub_contributors = get_contributor('https://www.openhub.net/p/' + repo_name + '/contributors/summary')

    contributors = mess(json.dumps(contributors), openhub_contributors)
    # for contributor in contributors:
    #     retry = 100
    #     streak = None
    #     while retry != 0:
    #         try:
    #             print("try!!!" + contributor['login'])
    #             streak = get_streak(contributor['login'])
    #             print("getgetget!!!" + contributor['login'])
    #             break
    #         except:
    #             retry -= 1
    #             pass
    #     for k in streak:
    #         contributor[k] = streak[k]

    for commit in commits:
        ret, id = utils.create_node_with_id('commit_index', commit, 'Commit', 'commit_id', commit['sha'])

    for commit_file in commit_files:
        _, commit_id = utils.get_node('commit_index', 'commit_id', commit_file['commitSha'])
        ret, file_id = utils.create_node_with_id(None, commit_file, 'CommitFile', None, None)
        utils.create_relationship(commit_id, file_id, 'CHANGE_FILE')

    for contributor in contributors:
        ret, id = utils.create_node_with_id('contributor_index', contributor, 'Contributor', 'contributor_id', contributor['id'])

    for issue in issues:
        ret, id = utils.create_node_with_id('issue_index', issue, 'Issue', 'issue_id', issue['id'])

    for release in releases:
        ret, id = utils.create_node_with_id('release_index', release, 'Release', 'release_id', release['Releasid'])

    repo_id = -1
    for repo in repositories:
        ret, repo_id = utils.create_node_with_id('repository_index', repo, 'Repository', 'repository_id', repo['repositoryName'])
        repo_contributors = repo['contributors']
        repo_releases = repo['releases']
        repo_issues = repo['issues']
        repo_commits = repo['commits']
        for repo_contributor in [x.strip() for x in repo_contributors.split(',')]:
            _, contributor_id = utils.get_node('contributor_index', 'contributor_id', repo_contributor)
            utils.create_relationship(contributor_id, repo_id, 'CONTRIBUTE')
        for repo_release in [x.strip() for x in repo_releases.split(',')]:
            _, release_id = utils.get_node('release_index', 'release_id', repo_release)
            utils.create_relationship(repo_id, release_id, 'HAS_RELEASE')
        for repo_commit in [x.strip() for x in repo_commits.split(',')]:
            _, commit_id = utils.get_node('commit_index', 'commit_id', repo_commit)
            utils.create_relationship(repo_id, commit_id, 'HAS_COMMIT')
        for repo_issue in [x.strip() for x in repo_issues.split(',')]:
            _, issue_id = utils.get_node('issue_index', 'issue_id', repo_issue)
            utils.create_relationship(repo_id, issue_id, 'HAS_ISSUE')

    for tree in trees:
        # _, repo_id = utils.get_node('repository_index', 'repository_id', tree['ProjectName'])
        ret, project_id = utils.create_node_with_id(None, tree, 'Tree', None, None)
        utils.create_relationship(repo_id, project_id, 'HAS_FILE')

    for project in projects:
        # _, repo_id = utils.get_node('repository_index', 'repository_id', project['project_name'])
        ret, project_id = utils.create_node_with_id('project_index', project, 'Project', 'project_id', project['project_name'])
        utils.create_relationship(repo_id, project_id, 'HAS_PROJECT')

    for news in project_news:
        _, project_id = utils.get_node('project_index', 'project_id', project['project_name'])
        ret, news_id = utils.create_node_with_id(None, news, 'ProjectNews', None, None)
        utils.create_relationship(project_id, news_id, 'HAS_NEWS')

# content = None
# with open('json-sample.txt', 'r') as f:
#     content = ''.join(f.readlines())
# #content = unicode(content, errors='replace')
# content = content.decode("utf-8-sig")
# upload(json.loads(content))
