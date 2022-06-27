# encoding=UTF-8
"""
"""
import data
from table import a


JENKINS_ROOT_HTML = 'JENKINS_ROOT.htm'  # a suspect HTML that necessitated ATable (notice A_VALUE ">" prefix)


def test_from_text():
    text = data.text_from(JENKINS_ROOT_HTML)
    at = a.ATable.from_text(text)
    print()
    print(at.pf('at'))
    n = 0
    for col in at.col_gen():
        n += 1
        print(n, col)
    assert n == 25
