import os
import sys
import time
import random

CONTENT_PATH = './content/'
TEMPLATE_HTML = './template/template.html'
TEMPLATE_INDEX_HTML = './template/template_index.html'
INDEX_FILE = 'index'
SITE_TITLE = '凹凸环球尖货'

def parse_content(filename):
    title = ''
    content = ''
    group = ''
    imgs = []
    with open(CONTENT_PATH + filename) as f:
        for line in f:
            line = line[:-1]
            if (line.startswith('group:')):
                group = line[6:]
            elif (line.startswith('title:')):
                title = line[6:]
            elif (line.startswith('img:')):
                content += '<p><img src="'+line[4:]+'"></p>\n'
                imgs.append(line[4:])
            else:
                content += '<p>' + line + '</p>\n'
    return {'errcode':0, 'title':title, 'group':group, 'content':content, 'imgs':imgs, 'modify_ts':os.path.getmtime(CONTENT_PATH+filename)}

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

def output_html(filename, temp_html, title, content):
    temp_html = temp_html.replace('???title???', title)
    temp_html = temp_html.replace('???content???', content)
    f = open(filename+'.html', 'w')
    f.write(temp_html)
    f.close()

def process_index(group_list, newest_list, temp_html):
    index_body = ''

    #最近更新
    index_body += '<h3>最新尖货'+time.strftime('%m/%d') +'</h3>\n'
    for link in newest_list:
        index_body += '<a href="/'+link['file']+'.html"><img src="'+link['imgs'][0]+'"><br/>'+link['title']+'</a><p style="color:red;display:inline" class="tab blink">new!</p><br><br>\n'

    for group_name, group_item in group_list.items():
        index_body += '<h3>'+group_name+'</h3>\n'
        for link in group_item:
            index_body += '<a href="/'+link['file']+'.html"><img src="'+link['imgs'][0]+'"><br/>'+link['title']+'</a><br><br>\n'
    output_html(INDEX_FILE, temp_html, SITE_TITLE, index_body)

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
            result = parse_content(fn)
            if result['errcode'] == 0:
                result['file'] = fn
                link_list.append(result)

    # sort them with group
    group_list = {}
    newest_list = []
    expire_ts = time.time() - 1300; #two days expire
    for link in link_list:
        if 'modify_ts' in link:
            if link['modify_ts'] > expire_ts and len(newest_list) < 5:
                newest_list.append(link)
        if 'group' in link:
            if link['group'] not in group_list:
                group_list[link['group']] = []
            group_list[link['group']].append(link)
        else:
            if '其他' not in group_list:
                group_list['其他'] = []
            group_list['其他'].append(link)

    # output all content page
    for link in link_list:
        #recommend same group item
        if len(group_list[link['group']]) > 2:
            link['content'] += '<hr><h2>猜你喜欢</h2>'
            for recommend in random.sample(group_list[link['group']], 3):
                if link['title'] == recommend['title']:
                    continue
                link['content'] += '<p><a href="/'+recommend['file']+'.html?from=recommend">'+recommend['title']+'</a></p>'
        output_html(link['file'], temp_html, link['title'], link['content'])
        print("Finish:"+link['file']+" title:"+link["title"])

    #load template for index page
    temp_index_html = load_temp_index()
    if (temp_index_html == ''):
        print('FATAL: template html for index file not found!')
        return
    # process the index
    process_index(group_list, newest_list, temp_index_html)
    print('Finish the index page generate!')

if __name__ == '__main__':
    main()
