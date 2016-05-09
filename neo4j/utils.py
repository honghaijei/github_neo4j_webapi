import urllib2
import base64
import json
from urllib import quote
import datetime
from lxml import etree

end_point = "http://10.60.45.67:7474"


def create_node_with_id(index_name, properties, label, key, value):
    try:
        if index_name != None:
            data = { "key" : key, "value" : value, "properties" : properties }
            request = urllib2.Request(end_point + "/db/data/index/node/" + index_name + "?uniqueness=create_or_fail", json.dumps(data))
            base64string = base64.encodestring('%s:%s' % ("neo4j", "123456")).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)
            request.add_header("Accept", "application/json; charset=UTF-8")
            request.add_header("Content-Type", "application/json")
            result = urllib2.urlopen(request)
        else:
            request = urllib2.Request(end_point + "/db/data/node/", json.dumps(properties))
            base64string = base64.encodestring('%s:%s' % ("neo4j", "123456")).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)
            request.add_header("Accept", "application/json; charset=UTF-8")
            request.add_header("Content-Type", "application/json")
            result = urllib2.urlopen(request)
        res_code = result.getcode()
        if res_code != 201:
            return res_code, None
        respond_js = json.loads(result.read())
        node_id = respond_js['metadata']['id']
        labels = [label]
        request = urllib2.Request(end_point + "/db/data/node/" + str(node_id) + "/labels", json.dumps(labels))
        base64string = base64.encodestring('%s:%s' % ("neo4j", "123456")).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header("Accept", "application/json; charset=UTF-8")
        request.add_header("Content-Type", "application/json")
        result = urllib2.urlopen(request)
        res_code = result.getcode()
        if res_code == 204:
            return None, respond_js['metadata']['id']
        return res_code, None
    except Exception as e:
        return e.code, None


def create_node(index_name, properties, label, key, value):
    return create_node_with_id(index_name, properties, label, key, value)[0]


def create_relationship(node_id1, node_id2, rel_type):
    try:
        data = { "to" : end_point + "/db/data/node/" + str(node_id2), "type": rel_type}
        request = urllib2.Request(end_point + "/db/data/node/" + str(node_id1) + "/relationships", json.dumps(data))
        base64string = base64.encodestring('%s:%s' % ("neo4j", "123456")).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header("Accept", "application/json; charset=UTF-8")
        request.add_header("Content-Type", "application/json")
        result = urllib2.urlopen(request)
        ret_code = result.getcode()
        if ret_code == 201:
            return None
        else:
            return ret_code
    except Exception as e:
        return e.code


def get_node(index_id, key, value):
    request = urllib2.Request(end_point + "/db/data/index/node/"+index_id+"/"+key+"/"+quote(value))
    base64string = base64.encodestring('%s:%s' % ("neo4j", "123456")).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    request.add_header("Accept", "application/json; charset=UTF-8")
    result = urllib2.urlopen(request)
    res_read = result.read()
    res = json.loads(res_read)
    if len(res) != 1:
        return None, None
    else:
        return res[0]['data'], res[0]['metadata']['id']

def get_page(url):
    request = urllib2.Request(url)
    request.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36")
    result = urllib2.urlopen(request, timeout=30)
    return result.read()


date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime)
    or isinstance(obj, datetime.date)
    else None
)


def get_streak(id):
    user_page = etree.HTML(get_page('https://github.com/' + id).lower().decode('utf-8'))
    sta = user_page.xpath(u'.//span[@class="contrib-number"]');
    longest_streak = sta[1].text
    current_streak = sta[2].text
    return { "longest_streak": longest_streak, "current_streak": current_streak }

