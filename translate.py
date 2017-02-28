import os
import sys
import time

CONTENT_PATH = './content/'
TEMPLATE_HTML = './template/template.html'
TEMPLATE_INDEX_HTML = './template/template_index.html'
INDEX_FILE = 'index'
SITE_TITLE = '凹凸香港尖货推荐'

def process_content(filename, temp_html):
    head = ''
    body = ''
    group = ''
    with open(CONTENT_PATH + filename) as f:
        for line in f:
            line = line[:-1]
            if (line.startswith('group:')):
                group = line[6:]
            elif (line.startswith('title:')):
                head = line[6:]
            elif (line.startswith('img:')):
                body += '<img src="'+line[4:]+'">\n'
            else:
                body += '<p>' + line + '</p>\n'
    temp_html = temp_html.replace('???title???', head)
    temp_html = temp_html.replace('???content???', body)
    return {'errcode':0, 'head':head, 'html':temp_html, 'group':group, 'modify_ts':os.path.getmtime(CONTENT_PATH+filename)}

def load_template(temp_file):
    temp_html = ''
    if os.path.isfile(temp_file):
        with open(temp_file) as template:
            for line in template:
                temp_html += line
    return temp_html

def load_temp_detail():
    return load_template(TEMPLATE_HTML)

def load_temp_index():
    return load_template(TEMPLATE_INDEX_HTML)

def output_html(filename, html_content):
    f = open(filename+'.html', 'w')
    f.write(html_content)
    f.close()

def process_index(link_list, temp_html):
    index_body = ''
    group_list = {}
    newest_list = []
    expire_ts = time.time() - 2*24*3600; #two days expire
    for link in link_list:
        if 'modify_ts' in link:
            if link['modify_ts'] > expire_ts:
                newest_list.append(link)
        if 'group' in link:
            if link['group'] not in group_list:
                group_list[link['group']] = []
            group_list[link['group']].append(link)
        else:
            if '其他' not in group_list:
                group_list['其他'] = []
            group_list['其他'].append(link)

    #最近更新
    index_body += '<h3>最新尖货'+time.strftime('%m/%d') +'</h3>\n'
    for link in newest_list:
        index_body += '<a href="/'+link['file']+'.html">'+link['head']+'</a><p style="color:red;display:inline" class="tab blink">new!</p><br><br>\n'

    for group_name, group_item in group_list.items():
        index_body += '<h3>'+group_name+'</h3>\n'
        for link in group_item:
            index_body += '<a href="/'+link['file']+'.html">'+link['head']+'</a><br><br>\n'
    temp_html = temp_html.replace('???title???', SITE_TITLE)
    temp_html = temp_html.replace('???content???', index_body)
    output_html(INDEX_FILE, temp_html)

def main():
    # load template for content page
    temp_html = load_temp_detail()
    if (temp_html == ''):
        print('FATAL: template html file not found!')
        return

    link_list = []
    # open all content file in loop
    for fn in os.listdir(CONTENT_PATH):
        print('found one file:'+fn)
        if os.path.isfile(CONTENT_PATH+fn):
            result = process_content(fn, temp_html)
            if result['errcode'] == 0:
                output_html(fn, result['html'])
                print("Finish:"+fn+" title:"+result["head"])
                result['file'] = fn
                link_list.append(result)

    #load template for index page
    temp_index_html = load_temp_index()
    if (temp_index_html == ''):
        print('FATAL: template html for index file not found!')
        return
    # process the index
    process_index(link_list, temp_index_html)
    print('Finish the index page generate!')

if __name__ == '__main__':
    main()
