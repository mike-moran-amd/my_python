# encoding=UTF-8
"""
"""
import data
from table import a


JENKINS_ROOT_HTML = 'JENKINS_ROOT.htm'  # a suspect HTML that necessitated ATable (notice A_VALUE ">" prefix)


def test_test():
    text = data.text_from(JENKINS_ROOT_HTML)
    t = a.ATable.from_text(text)
    print()
    print(t.pf('t'))
    print(list(t.col_gen()))
