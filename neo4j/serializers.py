from rest_framework import serializers
from neo4j.models import Project, Developer, Commit, Code, Assessment, Cost, Issue, Document, Language, Repository, News
import urllib2
import base64
import json

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project


class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer


class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment

class CostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cost

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News





'''
class ProjectSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    project_id = serializers.CharField()
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        data = { "resttest" : "xxx" }
        
        request = urllib2.Request("http://10.60.45.67:7474/db/data/node", json.dumps(validated_data))
        base64string = base64.encodestring('%s:%s' % ("neo4j", "123456")).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header("Accept", "application/json; charset=UTF-8")
        request.add_header("Content-Type", "application/json")
        result = urllib2.urlopen(request)
	r = json.loads(result.read())
	node_id = r['metadata']['id']      
  
	data = "[ \"Project\"]"
        request = urllib2.Request("http://10.60.45.67:7474/db/data/node/" + str(node_id) + "/labels", data)
        base64string = base64.encodestring('%s:%s' % ("neo4j", "123456")).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header("Accept", "application/json; charset=UTF-8")
        request.add_header("Content-Type", "application/json")
        result = urllib2.urlopen(request)
        return validated_data

    def update(self, instance, validated_data):
        
        return instance
'''

'''
    def get_all_project(self):
	request = urllib2.Request("http://10.60.45.67:7474/db/data/label/Project/nodes")
        base64string = base64.encodestring('%s:%s' % ("neo4j", "123456")).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header("Accept", "application/json; charset=UTF-8")
        request.add_header("Content-Type", "application/json")
        result = urllib2.urlopen(request)
        r = json.loads(result.read())
	dicts = [i['data'] for i in r]
        res = []
	for dic in dicts:
            item = Project()
            item.project_id = dic['project_id']
            item.created = dic['created']
            item.title = dic['title']
            item.code = dic['code']
            item.linenos = dic['linenos']
            item.language = dic['language']
            item.style = dic['style']
            res.append(item)
        return res
'''
