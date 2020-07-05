# version 0.3


import regex as re

import urllib.parse

from aqt import mw
from anki import hooks

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

kanjiRep = re.compile(r'(\p{IsHan})', re.UNICODE)

def kanjiLink(st):
    stClean = remove_tags(st)
    stOut = kanjiRep.sub('<a href=\'javascript:pycmd("klink:\\1");\'>\\1</a>', stClean)
    print ("output from kanji link [%s]"%stOut)
#    st2 = kanjiRep.sub('<a href="%s\\1%20%23kanji">\\1</a>'%(jishoDictURL),stClean)
    return stOut

def doJishoKanji(st):
    stClean = remove_tags(st)
    stOut = kanjiRep.sub('<a href="%s\\1%20%23kanji">\\1</a>'%(jishoDictURL),stClean)
    print ("output from doJishoKanji [%s]"%stOut)
    return stOut


def doJisho(st):
    stClean = remove_tags(st)
    queryStr = urllib.parse.quote(stClean, safe='')
    return "<span class='dictionary'>(<a href='%s%s'>%s</a>)</span>"%(jishoDictURL, queryStr, queryStr)


def linktrans_do_field(fieldText, fieldName, filterName, context):

    if filterName == "linktrans":
        return translateLink(fieldText)
    elif filterName == "jisho":
        return doJisho(fieldText)
    elif filterName == "jishok":
        return doJishoKanji(fieldText)
    else:
        return fieldText

hooks.field_filter.append(linktrans_do_field)
#hooks.card_did_render.append(on_card_did_render)

# handle searching for kanji

def handle_kanji_command(handled, cmd, context):
    print("my command [%s]\n"%cmd)
    prefix = "klink:"
    if not cmd.startswith(prefix):
        return handled
    search = cmd[len(prefix):]
    browser = dialogs.open("Browser", mw)
    browser.form.searchEdit.lineEdit().setText(search)
    browser.onSearchActivated()
    return (True, None)

gui_hooks.webview_did_receive_js_message.append(handle_kanji_command)
