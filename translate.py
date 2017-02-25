import os
import sys

CONTENT_PATH = './content/'
TEMPLATE_HTML = './template.html'
INDEX_FILE = 'index'
SITE_TITLE = '凹凸香港尖货推荐'

def process_content(filename, temp_html):
    head = ''
    body = ''
    with open(CONTENT_PATH + filename) as f:
        for line in f:
            line = line[:-1]
            if (line.startswith('title:')):
                head = line[6:]
            elif (line.startswith('img:')):
                body += '<img src="'+line[4:]+'">\n'
            else:
                body += '<p>' + line + '</p>\n'
    temp_html = temp_html.replace('???title???', head)
    temp_html = temp_html.replace('???content???', body)
    return {'errcode':0, 'head':head, 'html':temp_html}

def load_template():
    temp_html = ''
    if os.path.isfile(TEMPLATE_HTML):
        with open(TEMPLATE_HTML) as template:
            for line in template:
                temp_html += line+'\n'
    return temp_html

def output_html(filename, html_content):
    f = open(filename+'.html', 'w')
    f.write(html_content)
    f.close()

def process_index(link_list, temp_html):
    index_body = ''
    for link in link_list:
        index_body += '<a href="/'+link['file']+'.html">'+link['head']+'</a><br>\n'
    temp_html = temp_html.replace('???title???', SITE_TITLE)
    temp_html = temp_html.replace('???content???', index_body)
    output_html(INDEX_FILE, temp_html)

def main():
    # load template
    temp_html = load_template()
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

    # process the index
    process_index(link_list, temp_html)

if __name__ == '__main__':
    main()
