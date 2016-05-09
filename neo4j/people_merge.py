import json
def mess(mes_git, mes_open):
    merge_data = []
    data_git = json.loads(mes_git)
    data_open = mes_open
    for i in xrange(len(data_git)):
        contributor_git = data_git[i]
        for j in xrange(len(data_open)):
            found = False
            contributor_open = data_open[j]
            if contributor_git['name'] == contributor_open['name']:
                final_data = merge(contributor_git,contributor_open)
                merge_data.append(final_data)
                found = True
                break;
        if found == False:
            print 'did not found contributor + ' + contributor_git['name']
    return merge_data

def merge(data_git, data_open):
    if 'personal homepage' in data_open:
        data_git['personal homepage'] = data_open['personal homepage']
    if 'corporation' in data_open:
        data_git['corporation'] = data_open['corporation']
    if 'Number of writing project description' in data_open:
        data_git['Number of writing project description'] = data_open['Number of writing project description']
    if 'Number of writing project  repository information' in data_open:
        data_git['Number of writing project  repository information'] = data_open['Number of writing project  repository information']
    if 'Manage Projects Number' in data_open:
        data_git['Manage Projects Number'] = data_open['Manage Projects Number']
    if 'Stacker' in data_open:
        data_git['Stacker'] = data_open['Stacker']
    if 'Number of Organization Management' in data_open:
        data_git['Number of Organization Management'] = data_open['Number of Organization Management']
    if 'Number of contributing FOSSer' in data_open:
        data_git['Number of contributing FOSSer'] = data_open['Number of contributing FOSSer']
    if 'Number of wrinting tag and classification different projects' in data_open:
        data_git['Number of wrinting tag and classification different projects'] = data_open['Number of wrinting tag and classification different projects']
    if 'Kudo' in data_open:
        data_git['Kudo'] = data_open['Kudo']
    return data_git