from lxml import etree
import json
from utils import get_page
import datetime


def get_project(name):
    project_page = etree.HTML(get_page('https://www.openhub.net/p/' + name).decode('utf-8'))

    project_name = project_page.xpath(u"//*[@id=\"project_header\"]/div[1]/h1/a")[0].text
    project_tag = project_page.xpath(u"//*[@id=\"project_tags\"]/p")[0].text

    similar_projects = project_page.xpath(u"//*[@id=\"similar_projects\"]")[0].text

    manager = project_page.xpath(u"//*[@id=\"page_contents\"]/div[3]/div[2]/div/dl/dd[5]/a")[0].text

    licenses = project_page.xpath(u"//*[@id=\"page_contents\"]/div[3]/div[2]/div/dl/dd[3]")[0].text

    location_page = etree.HTML(get_page('https://www.openhub.net/p/' + name + '/enlistments').decode('utf-8'))

    location_table = location_page.xpath(u"//table//tbody")[0]
    locations = [c.getchildren()[0].text.strip() for c in location_table.getchildren()]
    code_location = '\t'.join(locations)
    project = {"update_time": datetime.datetime.now().isoformat(), "project_name": project_name, "project_tag": project_tag, "similar_projects": similar_projects, "manager": manager, "licenses": licenses, "code_location": code_location }
    for key in project:
        if project[key] is None:
            project[key] = ''
    return project


# //*[@id="analyses_language_table"]