from lxml import etree
import urllib2
import json
from utils import get_page
import datetime


def get_project_news(name):
    project_page = etree.HTML(get_page('https://www.openhub.net/p/' + name).decode('utf-8'))

    project_age = project_page.xpath(u"//*[@id=\"factoids\"]/li[3]/div/span[1]/a")[0].text.strip()

    team_size = project_page.xpath(u"//*[@id=\"factoids\"]/li[1]/div/a[2]")[0].text.strip()

    project_activity = project_page.xpath(u"//*[@id=\"project_header_activity_indicator\"]/div")[0].text.strip()

    factoids_page = etree.HTML(get_page('https://www.openhub.net/p/' + name + '/factoids').decode('utf-8'))
    comments = ''.join(factoids_page.xpath(u"//*[@id=\"page_contents\"]")[0].itertext()).replace(u'\xa0', '').strip()

    # team_size_per_month = project_page.xpath(u"//*[@id=\"factoids\"]/li[3]/div/span[2]/a")[0].text
    # print(team_size_per_month)

    # contributor = project_page.xpath(u"")[0].text
    # print(contributor)

    ratings_page = etree.HTML(get_page('https://www.openhub.net/p/' + name + '/reviews/summary').decode('utf-8'))
    community_score = ratings_page.xpath(u"//*[@id=\"average_rating_details_2\"]")[0].text.replace(u'\xa0', '').strip()

    cost_page = etree.HTML(get_page('https://www.openhub.net/p/' + name + '/estimated_cost').decode('utf-8'))
    costs =  [''.join(i.itertext()).strip().replace(',', '').split('\n') for i in cost_page.xpath('.//div[@class="controls"]')][1:]
    lines =  [i.attrib['value'] for i in cost_page.xpath('.//option')]
    codebase_size = int(costs[0][0])
    estimated_effort = int(costs[1][0])
    estimated_cost = int(costs[2][1])

    cocomo = { 'codebase_size': codebase_size, 'estimated_effort': estimated_effort, 'estimated_cost': estimated_cost, "all_code": lines[0], 'logic_code_only': lines[1], 'markup_only': lines[2], 'build_scripts_only': lines[3] }


    language_page = etree.HTML(get_page('https://www.openhub.net/p/' + name + '/analyses/latest/languages_summary').decode('utf-8'))

    languages_table = language_page.xpath(u"//*[@id=\"analyses_language_table\"]")[0]
    data = [x for c in languages_table.getchildren() for x in c.getchildren()][2:-2]
    data = [[''.join(j.itertext()).strip() for j in i.getchildren()][1:] for i in data]

    languages = [{"code_name": line[0], "code_lines": line[1], "comment_lines": line[2], "comment_ratio": line[3], "blank_lines" : line[4], "total_lines": line[5], "total_percentage" : line[6]} for line in data]


    project_news = {"update_time": datetime.datetime.now().isoformat(), 'team_size': team_size, 'project_age': project_age, 'activity': project_activity, 'comments': comments, 'languages': json.dumps(languages), 'cost': json.dumps(cocomo) }
    for key in project_news:
        if project_news[key] is None:
            project_news[key] = ''
    return project_news