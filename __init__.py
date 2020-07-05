# version 0.3


import re

import urllib.parse

from anki import hooks
from aqt import dialogs, gui_hooks, mw


googleTransURL= 'https://translate.google.com/#view=home&op=translate&sl=ja&tl=en&text='
deepLTransURL=  'https://www.deepl.com/en/translator#jp/en/'
jishoDictURL=  'https://jisho.org/search/'

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
"""%(googleTransURL, queryStr, googleStr, deepLTransURL, queryStr, deepLStr)

kanjiRep = re.compile(r'([\u4E00-\u9FFF])', re.UNICODE)
hashChar = '%23'

def doKanjiLink(st):
    stClean = remove_tags(st)
    stOut = kanjiRep.sub('<a href=\'javascript:pycmd("klink:\\1");\'>\\1</a>', stClean)
    return stOut

def doJishoKanji(st):
    stClean = remove_tags(st)
    stOut = kanjiRep.sub('<a href="%s\\1 %skanji">\\1</a>'%(jishoDictURL, hashChar),stClean)
    return stOut

def doJisho(st):
    stClean = remove_tags(st)
    queryStr = urllib.parse.quote(stClean, safe='')
    return "<span class='dictionary'>(<a href='%s%s'>%s</a>)</span>"%(jishoDictURL, queryStr, st)

def linktrans_do_field(fieldText, fieldName, filterName, context):
    if filterName == "linktrans":
        return translateLink(fieldText)
    elif filterName == "jisho":
        return doJisho(fieldText)
    elif filterName == "jishok":
        return doJishoKanji(fieldText)
    elif filterName == "kbrowse":
        return doKanjiLink(fieldText)
    else:
        return fieldText

hooks.field_filter.append(linktrans_do_field)
#hooks.card_did_render.append(on_card_did_render)

# handle searching for kanji

kLinkPrefix = 'klink:'

def handle_kanji_command(handled, cmd, context):
    if not cmd.startswith(kLinkPrefix):
        return handled
    search = 'kanji:' + cmd[len(kLinkPrefix):].strip()
    browser = dialogs.open("Browser", mw)
    browser.form.searchEdit.lineEdit().setText(search)
    browser.onSearchActivated()
    return (True, None)

gui_hooks.webview_did_receive_js_message.append(handle_kanji_command)
