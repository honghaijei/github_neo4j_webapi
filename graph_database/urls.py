"""graph_database URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from neo4j import views as neo4j_views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^projects/(?P<project_id>.+)/$', neo4j_views.ProjectDetail.as_view()),
    url(r'^github_projects/', neo4j_views.GitHubProject.as_view(), name = 'github_projects_url'),
    url(r'^projects/(?P<project_id>.+)/$', neo4j_views.ProjectDetail.as_view()),
    url(r'^projects/', neo4j_views.ProjectList.as_view(), name = 'projects_url'),
    
    url(r'^developers/(?P<developer_id>.+)/$', neo4j_views.DeveloperDetail.as_view()),
    url(r'^developers/', neo4j_views.DeveloperList.as_view(), name = 'developers_url'),
    url(r'^commits/', neo4j_views.CommitList.as_view(), name = 'commits_url'),
    url(r'^codes/', neo4j_views.CodeList.as_view(), name = 'codes_url'),
    url(r'^assessments/', neo4j_views.AssessmentList.as_view(), name = 'assessments_url'),
    url(r'^costs/', neo4j_views.CostList.as_view(), name = 'costs_url'),
    url(r'^issues/', neo4j_views.IssueList.as_view(), name = 'issues_url'),
    url(r'^documents/', neo4j_views.DocumentList.as_view(), name = 'documents_url'),
    url(r'^languages/', neo4j_views.LanguageList.as_view(), name = 'languages_url'),
    url(r'^repositories/', neo4j_views.RepositoryList.as_view(), name = 'repositories_url'),
    url(r'^news/', neo4j_views.NewsList.as_view(), name = 'news_url'),
]
