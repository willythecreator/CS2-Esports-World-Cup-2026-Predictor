import re

html = open('data/raw/9c27aeab8891993838bd2b6cbcbd13aa.html', encoding='utf-8').read()
idx = html.find('2396006')
print(html[idx-200:idx+1500])