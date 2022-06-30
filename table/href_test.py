# encoding=UTF-8
"""
"""
import data
from table.href import HrefTable
from table.a import ATable


JENKINS_ROOT_HTML = 'JENKINS_ROOT.htm'  # a suspect HTML that necessitated ATable (notice A_VALUE ">" prefix)


def test_from_a_table():
    text = data.text_from(JENKINS_ROOT_HTML)
    at = ATable.from_text(text)
    ht = HrefTable.from_a_table(at, href_starts_with='job/')
    print()
    print(ht.pf('ht'))


def test_from_text():
    text = data.text_from(JENKINS_ROOT_HTML)
    ht = HrefTable.from_text(text, href_starts_with='job/')
    print()
    print(ht.pf('ht'))


def test_get_href_and_value():
    print()
    text = data.text_from(JENKINS_ROOT_HTML)
    ht = HrefTable.from_text(text, href_starts_with='job/')
    for row in ht.row_gen():
        href = ht.get_href(row)
        href_value = ht.get_href_value(row)
        if href.endswith('lastSuccessfulBuild/') or href.endswith('lastFailedBuild/'):
            print(href_value[2:], href.split('/')[1:3])
