import re
import urllib2
import Queue
from bs4 import BeautifulSoup
import logging

q = Queue.Queue(maxsize=1000)
people_page = Queue.Queue(maxsize=1000)
people_exist = {}
#log
logger = logging.getLogger('getPeoplelog')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('peoplelog.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

def get_contributor_url(firsr_url):
    url = firsr_url
    while url is not None:
        contributor_content = None
        while contributor_content == None:
            try:
                request = urllib2.Request(url)
                request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
                request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36')
                contributor_content = urllib2.urlopen(request,timeout=10).read()
                soup = BeautifulSoup(contributor_content, "lxml")
                content = soup.find_all(class_ = "avatar_name pull-left col-md-10 padding_left_0")
                for link in content:
                    link_str = link.get('href')
                    if link_str is None:
                        continue
                    contributor_id = re.search("^/p/.*/contributors/(\d*)", link_str)

                    if contributor_id is not None:
                        id = contributor_id.group(1)
                        if not (id in people_exist):
                            people_exist[id] = 1
                            q.put("https://www.openhub.net" + link_str)
                            print 'get contributor url ' + id
                #get next page
                next_page_tag = soup.find(rel='next')
                if next_page_tag is not None:
                    url = 'https://www.openhub.net' + next_page_tag.get('href')
                else:
                    #final page
                    url = None
            except:
                continue

def get_contributor_page():
    result = None
    url = q.get()
    while result == None:
        try:
            if url is not None:
                request = urllib2.Request(url)
                request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
                request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36')
                result = urllib2.urlopen(request, timeout=10)
                if result != None:
                    page_content = result.read()
                    people_page.put(page_content)
                    break
        except:
            result = None
            continue


def get_content():
    isUser = False
    data = {}
    content = people_page.get()
    soup = BeautifulSoup(content, "lxml")

    # get href
    for link in soup.find_all('a'):
        link_str = link.get('href')
        if link_str is None:
            continue

        ma = re.findall(r'^/accounts/[^/]+', link_str)
        if ma is not None:
            for link in ma:
                if link == '/accounts/me':
                    continue
                else:
                    # is an openhub user
                    isUser = True
                    personal_link = "https://www.openhub.net" + link
                    data = get_user_content(personal_link)
                    print 'get a user content ' + personal_link
                    if data.__len__() == 0:
                        print personal_link + ' data len is zero'
    if isUser == False:
        #is not an openhub user
        # getname
        name_tag = soup.find(class_="pull-left contributor_name margin_top_20")
        if name_tag is not None:
            soup_tmp = BeautifulSoup(str(name_tag), "lxml")
            name_str = soup_tmp.get_text()
            ma = re.search(r'\nContributors\s:\s\n(.*)', name_str)
            if ma is not None:
                name = ma.group(1)
                data['name'] = name
        else:
            pass
        # get kudo
        for tag in soup.find_all('img'):
            kudo_tag = tag.get('alt')
            if kudo_tag is not None:
                ma = re.search(r'^KudoRank\s(\d*)$', str(kudo_tag))
                if ma is not None:
                    kudo_level = ma.group(1)
                    data['Kudo'] = kudo_level
    return data

def get_user_content(personal_link):
    user_data={}
    content = None
    while content == None:
        try:
            request = urllib2.Request(personal_link)
            request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
            request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36')
            content = urllib2.urlopen(request,timeout=10).read()
        except:
            continue
    soup = BeautifulSoup(content, 'lxml')
    #get name
    name_tag = soup.find(itemprop='name')
    if name_tag is not None:
        name = name_tag.get_text()
        user_data['name'] = name
    #get homepage
    homepage_tag = soup.find(class_='icon-external-link')
    if homepage_tag is not None:
        homepage = homepage_tag.get_text().strip()
        user_data['personal homepage'] = homepage

    #get corporation
    par_corporation_tag = soup.find_all(class_='info')
    for tag in par_corporation_tag:
        ma = re.search(r'<a href=\"/orgs/\d*\">(.*)</a>', str(tag))
        if ma is not None:
            corporation = ma.group(1)
            user_data['corporation'] = corporation
        else:
            continue

    #get Describer
    describer_tag = soup.find(class_='pull-left account-badge describer-badge')
    if describer_tag is not None:
        title = describer_tag.get('title')
        ma = re.match(r'Level\s(\d*)\sDescriber', title)
        if ma is not None:
            describer_level = ma.group(1)
            user_data['Number of writing project description'] = describer_level

    #get repo
    repo_tag = soup.find(class_='pull-left account-badge repo-person-badge')
    if repo_tag is not None:
        title = repo_tag.get('title')
        ma = re.match(r'Level\s(\d*)\sRepo', title)
        if ma is not None:
            repo = ma.group(1)
            user_data['Number of writing project  repository information'] = repo

    #get cheese
    cheese_tag = soup.find(class_= 'pull-left account-badge project-manager-badge')
    if cheese_tag is not None:
        cheese = 1
        user_data['Manage Projects Number'] = cheese

    # get stacker
    stacker_tag = soup.find(class_='pull-left account-badge stacker-badge last')
    if stacker_tag is not None:
        title = stacker_tag.get('title')
        ma = re.match(r'Level\s(\d*)\sStacker',title)
        if ma is not None:
            stacker = ma.group(1)
            user_data['Stacker'] = stacker

    # get org
    org_tag = soup.find(class_='pull-left account-badge org-manager-badge')
    if org_tag is not None:
        org = 1
        user_data['Number of Organization Management'] = org

    # get FLOSSER
    Fosser_tag = soup.find(class_='pull-left account-badge fos-ser-badge')
    if Fosser_tag is not None:
        title = Fosser_tag.get('title')
        ma = re.match(r'Level\s(\d*)\sFLOSSer',title)
        if ma is not None:
            foss = ma.group(1)
            user_data['Number of contributing FOSSer'] = foss
    # get TAX
    TAX_tag = soup.find(class_='pull-left account-badge taxonomist-badge')
    if TAX_tag is not None:
        title = TAX_tag.get('title')
        ma = re.match(r'Level\s(\d*)\sTAX',title)
        if ma is not None:
            TAX = ma.group(1)
            user_data['Number of wrinting tag and classification different projects'] = TAX

    # get kudo
    kudo_tag = soup.find(class_='pull-left account-badge kudo-rank-badge last')
    if kudo_tag is not None:
        title = kudo_tag.get('title')
        ma = re.match(r'Level\s(\d*)\sKudo',title)
        if ma is not None:
            kudo = ma.group(1)
            user_data['Kudo'] = kudo

    return user_data

def get_contributor(init_contributor_url):
    all_user_data=[]
    ma = re.search(r'(https://www.openhub.net/p/.*/)summary', init_contributor_url)
    if ma is not None:
        contributor_url = ma.group(1)
    get_contributor_url(contributor_url)
    while 0!=q.qsize():
        get_contributor_page()
    while 0 != people_page.qsize():
        user_data = get_content()
        all_user_data.append(user_data)
    return all_user_data
