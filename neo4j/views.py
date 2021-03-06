from django.shortcuts import render
from neo4j.models import *
from neo4j.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
import neo4j.utils
import urllib2
import base64
import json
from upload import upload


class GitHubProject(APIView):
    def post(self, request, format=None):
        data=request.data
        # if serializer.is_valid():
        #     res = neo4j.utils.create_node("project_index", request.data, "Project", "project_id", request.data["project_id"])
        #     if res == None:
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     else:
        #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = json.dumps(data)
        print(data)
        proj = json.loads(str(data))
	
        # try:
        upload(proj)
        return Response("", status=status.HTTP_201_CREATED)
        # except:
        #     return Response("", status=status.HTTP_400_BAD_REQUEST)


class ProjectList(APIView):
    """
    List all projects, or create a new project.
    """
    def get(self, request, format=None):
        return Response(neo4j.utils.get_all_nodes('Project'))

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            res = neo4j.utils.create_node("project_index", request.data, "Project", "project_id", request.data["project_id"])
            if res == None:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    """
    Retrieve, update or delete a project instance.
    """

    def get(self, request, project_id, format=None):
        res, _ = neo4j.utils.get_node("project_index", "project_id", project_id)
        if res != None:
            return Response(res)
        else:
            raise Http404
            


class DeveloperList(APIView):
    """
    List all developers, or create a new developer.
    """
    def get(self, request, format=None):
        return Response(neo4j.utils.get_all_nodes('Developer'))

    def post(self, request, format=None):
        serializer = DeveloperSerializer(data=request.data)
        if serializer.is_valid():
            res, dev_neo4j_id = neo4j.utils.create_node_with_id("developer_index", request.data, "Developer", "developer_id", request.data["developer_id"])
            if res == None:
                star = [i.strip() for i in request.data['starred_url'].split(",")]
                for cont in star:
                    _, proj_neo4j_id = neo4j.utils.get_node("project_index", "project_id", cont)
                    neo4j.utils.create_relationship(dev_neo4j_id, proj_neo4j_id, "STAR")

                subcribe = [i.strip() for i in request.data['subscriptions_url'].split(",")]
                for cont in subcribe:
                    _, proj_neo4j_id = neo4j.utils.get_node("project_index", "project_id", cont)
                    neo4j.utils.create_relationship(dev_neo4j_id, proj_neo4j_id, "SUBSCRIBE")

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeveloperDetail(APIView):
    """
    Retrieve, update or delete a developer instance.
    """

    def get(self, request, developer_id, format=None):
        res, _ = neo4j.utils.get_node("developer_index", "developer_id", developer_id)
        if res != None:
            return Response(res)
        else:
            raise Http404


class CommitList(APIView):
    """
    List all commits, or create a new commit.
    """
    def get(self, request, format=None):
        return Response(neo4j.utils.get_all_nodes('Commit'))

    def post(self, request, format=None):
        serializer = CommitSerializer(data=request.data)
        if serializer.is_valid():
            res = neo4j.utils.create_node("commit_index", request.data, "Commit", "commit_id", request.data["commit_id"])

            if res == None:
                _, proj_neo4j_id = neo4j.utils.get_node("project_index", "project_id", request.data["project_id"])
                _, comm_neo4j_id = neo4j.utils.get_node("commit_index", "commit_id", request.data["commit_id"])
                neo4j.utils.create_relationship(comm_neo4j_id, proj_neo4j_id, "PROJECT_COMMIT")
                
                contributors = [i.strip() for i in request.data['contributor'].split(",")]
                for cont in contributors:
                    _, dev_neo4j_id = neo4j.utils.get_node("developer_index", "developer_id", cont)
                    neo4j.utils.create_relationship(dev_neo4j_id, comm_neo4j_id, "CONTRIBUTE")
                
                _, author_neo4j_id = neo4j.utils.get_node("developer_index", "developer_id", request.data["author"])
                neo4j.utils.create_relationship(author_neo4j_id, comm_neo4j_id, "AUTHOR")
                return Response(serializer.data, status=status.HTTP_201_CREATED)

                codes = [i.strip() for i in request.data['files_modified'].split(",")]
                for cont in codes:
                    _, code_neo4j_id = neo4j.utils.get_node("code_index", "code_id", cont)
                    neo4j.utils.create_relationship(comm_neo4j_id, code_neo4j_id, "COMMIT_MODIFY")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommitDetail(APIView):
    """
    Retrieve, update or delete a commit instance.
    """

    def get(self, request, commit_id, format=None):
        res = neo4j.utils.get_node("commit_index", "commit_id", commit_id)
        if res != None:
            return Response(res)
        else:
            raise Http404



class CodeList(APIView):
    """
    List all codes, or create a new code.
    """
    def get(self, request, format=None):
        return Response(neo4j.utils.get_all_nodes('Code'))

    def post(self, request, format=None):
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid():
            res = neo4j.utils.create_node("code_index", request.data, "Code", "code_id", request.data["code_id"])
            if res == None:
                _, proj_neo4j_id = neo4j.utils.get_node("project_index", "project_id", request.data["project_id"])
                _, code_neo4j_id = neo4j.utils.get_node("code_index", "code_id", request.data["code_id"])
                neo4j.utils.create_relationship(code_neo4j_id, proj_neo4j_id, "PROJECT_CODE")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeDetail(APIView):
    """
    Retrieve, update or delete a code instance.
    """
    def get(self, request, code_id, format=None):
        res = neo4j.utils.get_node("code_index", "code_id", code_id)
        if res != None:
            return Response(res)
        else:
            raise Http404


class AssessmentList(APIView):
    """
    List all assesses, or create a new assess.
    """
    def get(self, request, format=None):
        return Response(neo4j.utils.get_all_nodes('Assessment'))

    def post(self, request, format=None):
        serializer = AssessmentSerializer(data=request.data)
        if serializer.is_valid():
            res, ass_neo_id = neo4j.utils.create_node_with_id(None, request.data, "Assessment", None, None)
            if res == None:
                _, proj_neo4j_id = neo4j.utils.get_node("project_index", "project_id", request.data["project_id"])
                neo4j.utils.create_relationship(proj_neo4j_id, ass_neo_id, "PROJECT_ASSESSMENT")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CostList(APIView):
    """
    List all costs, or create a new cost.
    """
    def get(self, request, format=None):
        return Response(neo4j.utils.get_all_nodes('Cost'))
    def post(self, request, format=None):
        serializer = CostSerializer(data=request.data)
        if serializer.is_valid():
            res, cost_neo_id = neo4j.utils.create_node_with_id(None, request.data, "Cost", None, None)
            if res == None:
                _, proj_neo4j_id = neo4j.utils.get_node("project_index", "project_id", request.data["project_id"])
                neo4j.utils.create_relationship(proj_neo4j_id, cost_neo_id, "PROJECT_COST")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueList(APIView):
    """
    List all defects, or create a new defect.
    """
    def get(self, request, format=None):
        return Response(neo4j.utils.get_all_nodes('Issue'))
    def post(self, request, format=None):
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            res = neo4j.utils.create_node("issue_index", request.data, "Issue", "issue_id", request.data["issue_id"])
            if res == None:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueDetail(APIView):
    """
    Retrieve, update or delete a issue instance.
    """
    def get(self, request, issue_id, format=None):
        res = neo4j.utils.get_node("issue_index", "issue_id", issue_id)
        if res != None:
            return Response(res)
        else:
            raise Http404


class DocumentList(APIView):
    """
    List all documents, or create a new document.
    """
    def get(self, request, format=None):
        return Response(neo4j.utils.get_all_nodes('Document'))
    def post(self, request, format=None):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            res, doc_neo_id = neo4j.utils.create_node_with_id('document_index', request.data, "Document", "document_id", request.data["document_id"])
            if res == None:
                _, proj_neo4j_id = neo4j.utils.get_node("project_index", "project_id", request.data["project_id"])
                print(proj_neo4j_id)
                print(doc_neo_id)
                neo4j.utils.create_relationship(proj_neo4j_id, doc_neo_id, "PROJECT_DOCUMENT")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentDetail(APIView):
    """
    Retrieve, update or delete a document instance.
    """
    def get(self, request, issue_id, format=None):
        res = neo4j.utils.get_node("document_index", "document_id", document_id)
        if res != None:
            return Response(res)
        else:
            raise Http404

class LanguageList(APIView):
    """
    List all languages, or create a new language.
    """
    def get(self, request, format=None):
        return Response(neo4j.utils.get_all_nodes('Language'))
    def post(self, request, format=None):
        serializer = LanguageSerializer(data=request.data)
        if serializer.is_valid():
            res, lang_neo_id = neo4j.utils.create_node_with_id('language_index', request.data, "Language", "language_id", request.data["language_id"])
            if res == None:
                _, proj_neo4j_id = neo4j.utils.get_node("project_index", "project_id", request.data["project_id"])
                neo4j.utils.create_relationship(proj_neo4j_id, lang_neo_id, "PROJECT_LANGUAGE")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LanguageDetail(APIView):
    """
    Retrieve, update or delete a language instance.
    """
    def get(self, request, language_id, format=None):
        res = neo4j.utils.get_node("language_index", "language_id", language_id)
        if res != None:
            return Response(res)
        else:
            raise Http404

class RepositoryList(APIView):
    """
    List all libraries, or create a new library.
    """
    def get(self, request, format=None):
        return Response(neo4j.utils.get_all_nodes('Repository'))
    def post(self, request, format=None):
        serializer = RepositorySerializer(data=request.data)
        if serializer.is_valid():
            res, repo_neo_id = neo4j.utils.create_node_with_id('repository_index', request.data, "Repository", "repository_id", request.data["repository_id"])
            if res == None:
                try:
                    commits = [i.strip() for i in request.data['commit_message'].split(",")]
                    for cont in commits:
                        _, commit_neo_id = neo4j.utils.get_node("commit_index", "commit_id", cont)
                        neo4j.utils.create_relationship(commit_neo_id, repo_neo_id, "COMMIT_REPO")
                
                    contributors = [i.strip() for i in request.data['contributors'].split(",")]
                    for cont in contributors:
                        _, dev_neo4j_id = neo4j.utils.get_node("developer_index", "developer_id", cont)
                        neo4j.utils.create_relationship(dev_neo4j_id, repo_neo_id, "CONTRIBUTE_REPO")

                    forks = [i.strip() for i in request.data['forks_url'].split(",")]
                    for cont in forks:
                        _, dev_neo4j_id = neo4j.utils.get_node("developer_index", "developer_id", cont)
                        neo4j.utils.create_relationship(dev_neo4j_id, repo_neo_id, "FORK_REPO")

                    issues = [i.strip() for i in request.data['issues_url'].split(",")]
                    for cont in issues:
                        _, issue_neo4j_id = neo4j.utils.get_node("issue_index", "issue_id", cont)
                        neo4j.utils.create_relationship(issue_neo4j_id, repo_neo_id, "ISSUE_REPO")
                except:
                    pass
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RepositoryDetail(APIView):
    """
    Retrieve, update or delete a repository instance.
    """
    def get(self, request, repository_id, format=None):
        res = neo4j.utils.get_node("repository_index", "repository_id", repository_id)
        if res != None:
            return Response(res)
        else:
            raise Http404

class NewsList(APIView):
    """
    List all news, or create a new news.
    """
    def get(self, request, format=None):
        return Response(neo4j.utils.get_all_nodes('News'))
    def post(self, request, format=None):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            res, news_neo_id = neo4j.utils.create_node_with_id(None, request.data, "News", None, None)
            if res == None:
                contributors = [i.strip() for i in request.data['contributor_number'].split(",")]
                for cont in contributors:
                    _, dev_neo4j_id = neo4j.utils.get_node("developer_index", "developer_id", cont)
                    neo4j.utils.create_relationship(dev_neo4j_id, news_neo_id, "CONTRIBUTE_NEWS")
                

                languages = [i.strip() for i in request.data['programming_language'].split(",")]
                for cont in languages:
                    _, lang_neo4j_id = neo4j.utils.get_node("language_index", "language_id", cont)
                    neo4j.utils.create_relationship(lang_neo4j_id, news_neo_id, "LANG_REPO")
                

                commits = [i.strip() for i in request.data['commit_id'].split(",")]
                for cont in commits:
                    _, comm_neo4j_id = neo4j.utils.get_node("commit_index", "commit_id", cont)
                    neo4j.utils.create_relationship(comm_neo4j_id, news_neo_id, "COMMIT_REPO")
                

                followers = [i.strip() for i in request.data['followers_url'].split(",")]
                for cont in followers:
                    _, dev_neo4j_id = neo4j.utils.get_node("developer_index", "developer_id", cont)
                    neo4j.utils.create_relationship(dev_neo4j_id, news_neo_id, "FOLLOW")
                


                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
class ProjectDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, project_id):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, project_id, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, project_id, format=None):
        Project = self.get_object(pk)
        serializer = SnippetSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''
