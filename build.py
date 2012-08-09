from amazonSearch import Amazon
from xml.dom.minidom import parse, parseString
a = Amazon()
a.fetch("my bloody valentine")
for album in a.albums:
    print album['artist'] + ' - ' + album['title'] + ': '+str(album['price']) + '    (' + album['URL'] + ')'
    print album['image']
    print '---------------------------'
