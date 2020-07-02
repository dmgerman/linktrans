import re
import urllib.parse

from aqt import mw
from anki import hooks

googleDictURL= 'https://translate.google.com/#view=home&op=translate&sl=ja&tl=en&text='
deepLDictURL=  'https://www.deepl.com/en/translator#jp/en/'

googleStr = 'Goo'
deepLStr = 'Deep'

htmlRe = re.compile(r'<[^>]+>')
def remove_tags(text):
    return htmlRe.sub('', text)


def translateLink(st):
    stClean = remove_tags(st)
    queryStr = urllib.parse.quote(stClean, safe='')

#https://translate.google.com/#view=home&op=translate&sl=ja&tl=en&text=%E6%9D%A5%E3%81%AA%E3%81%84
#https://www.deepl.com/en/translator#en/de/this%20is%20the%20end%20of%20the%20world

    return """<span class='translate'>&nbsp;(<a href='%s%s'>%s</a>)</span>
&nbsp;<span class='translate'>&nbsp;(<a href='%s%s'>%s</a>)</span>
"""%(googleDictURL, queryStr, googleStr, deepLDictURL, queryStr, deepLStr)


def linktrans_do_field(fieldText, fieldName, filterName, context):

    if filterName == "linktrans":
        return translateLink(fieldText)
    else:
        return fieldName

    return "invalid dmg-<field> named [%s] with contents [%s]"%(fieldName, fieldText)


hooks.field_filter.append(linktrans_do_field)
#hooks.card_did_render.append(on_card_did_render)
