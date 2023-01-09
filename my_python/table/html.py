"""
>>> counter = 0
>>> for tt in TableTable.from_text_gen(data.text_from('JENKINS_ROOT.htm')):
...     tt.print_repr_lines(f'{counter}')
...     counter += 1

"""
import re
from my_python import table, data
from xml.etree import ElementTree
NL = '\n'


def html_table_text_gen(html_text):
    """
    #>>> for text in html_table_text_gen(data.text_from('JENKINS_ROOT.htm')):
    ...     print(len(text), repr(text.replace(NL, ' ')))

    """
    tag = 'td'
    for table_text in re.findall(f'<{tag} (.+?)</{tag}>', html_text):
        yield table_text


def root_from(text=data.text_from('JENKINS_ROOT.htm')):
    """
    #>>> root_from()

    """
    root = ElementTree.fromstring(text)
    return root


class ElementTable(table.Table):
    """
    #>>> et = ElementTable.from_text(data.text_from('JENKINS_ROOT.htm'))
    #>>> et_227_235 = ElementTable(et.tup_gen(rows=range(227, 235)))
    #>>> et_227_235.print_repr_lines('')
    '    | beg  | tag                                                                            | tag_value               | end '
    '227 | 8720 | <table class="pane ">                                                          |                         | 8740'
    "228 | 8741 | <script src='/adjuncts/e774c451/lib/form/link/link.js' type='text/javascript'> |                         | 8818"
    '229 | 8819 | </script>                                                                      |                         | 8827'
    '230 | 8828 | <tr>                                                                           |                         | 8831'
    '231 | 8832 | <td class="pane" colspan="2">                                                  | No builds in the queue. | 8860'
    '232 | 8884 | </td>                                                                          |                         | 8888'
    '233 | 8889 | </tr>                                                                          |                         | 8893'
    '234 | 8894 | </table>                                                                       |                         | 8901'

    #>>> et_398_466 = ElementTable(et.tup_gen(rows=range(398, 466)))
    #>>> et_398_466.print_repr_lines('')
    '    | beg   | tag                                                                                                                                                                 | tag_value                                           | end  '
    '398 | 12799 | <table id="projectstatus" class="sortable pane bigtable stripped-odd ">                                                                                             |                                                     | 12869'
    '399 | 12870 | <tr class="header">                                                                                                                                                 |                                                     | 12888'
    '400 | 12889 | <th tooltip="Status of the last build">                                                                                                                             | &nbsp;&nbsp;S                                       | 12927'
    '401 | 12941 | </th>                                                                                                                                                               |                                                     | 12945'
    '402 | 12946 | <th tooltip="Weather report showing aggregated status of recent builds">                                                                                            | &nbsp;&nbsp;W                                       | 13017'
    '403 | 13031 | </th>                                                                                                                                                               |                                                     | 13035'
    '404 | 13036 | <th initialSortDir="down">                                                                                                                                          | Name                                                | 13061'
    '405 | 13066 | </th>                                                                                                                                                               |                                                     | 13070'
    '406 | 13071 | <th>                                                                                                                                                                | Last Success                                        | 13074'
    '407 | 13087 | </th>                                                                                                                                                               |                                                     | 13091'
    '408 | 13092 | <th>                                                                                                                                                                | Last Failure                                        | 13095'
    '409 | 13108 | </th>                                                                                                                                                               |                                                     | 13112'
    '410 | 13113 | <th>                                                                                                                                                                | Last Duration                                       | 13116'
    '411 | 13130 | </th>                                                                                                                                                               |                                                     | 13134'
    '412 | 13135 | <th width="1">                                                                                                                                                      |                                                     | 13148'
    '413 | 13150 | </th>                                                                                                                                                               |                                                     | 13154'
    '414 | 13155 | <th>                                                                                                                                                                |                                                     | 13158'
    '415 | 13160 | </th>                                                                                                                                                               |                                                     | 13164'
    '416 | 13165 | </tr>                                                                                                                                                               |                                                     | 13169'
    '417 | 13170 | <tr id="job_CCV0_NoSEV_Test" class=" job-status-blue">                                                                                                              |                                                     | 13223'
    '418 | 13224 | <td data="4">                                                                                                                                                       |                                                     | 13236'
    '419 | 13237 | <span style="width: 32px; height: 32px; " class="build-status-icon__wrapper icon-blue icon-lg">                                                                     |                                                     | 13331'
    '420 | 13332 | <span class="build-status-icon__outer">                                                                                                                             |                                                     | 13370'
    '421 | 13371 | <svg viewBox="0 0 24 24" tooltip="Success" focusable="false" class="svg-icon ">                                                                                     |                                                     | 13449'
    '422 | 13450 | <use href="/images/build-status/build-status-sprite.svg#build-status-static">                                                                                       |                                                     | 13526'
    '423 | 13527 | </use>                                                                                                                                                              |                                                     | 13532'
    '424 | 13533 | </svg>                                                                                                                                                              |                                                     | 13538'
    '425 | 13539 | </span>                                                                                                                                                             |                                                     | 13545'
    '426 | 13546 | <svg viewBox="0 0 24 24" tooltip="Success" focusable="false" class="svg-icon icon-blue icon-lg">                                                                    |                                                     | 13641'
    '427 | 13642 | <use href="/static/e774c451/images/build-status/build-status-sprite.svg#last-successful">                                                                           |                                                     | 13730'
    '428 | 13731 | </use>                                                                                                                                                              |                                                     | 13736'
    '429 | 13737 | </svg>                                                                                                                                                              |                                                     | 13742'
    '430 | 13743 | </span>                                                                                                                                                             |                                                     | 13749'
    '431 | 13750 | </td>                                                                                                                                                               |                                                     | 13754'
    '432 | 13755 | <td data="60" class="healthReport" onmouseover="this.className=\\'healthReport hover\\';return true;'
    '        " onmouseout="this.className=\\'healthReport\\';return true;"> |                                                     | 13917'
    '433 | 13918 | <a href="job/CCV0_NoSEV_Test/lastBuild" class="build-health-link">                                                                                                  |                                                     | 13983'
    '434 | 13984 | <svg viewBox="0 0 24 24" focusable="false" class="svg-icon icon-health-40to59 icon-lg">                                                                             |                                                     | 14070'
    '435 | 14071 | <use href="/static/e774c451/images/build-status/weather-sprite.svg#weather-cloudy">                                                                                 |                                                     | 14153'
    '436 | 14154 | </use>                                                                                                                                                              |                                                     | 14159'
    '437 | 14160 | </svg>                                                                                                                                                              |                                                     | 14165'
    '438 | 14166 | </a>                                                                                                                                                                |                                                     | 14169'
    '439 | 14170 | <div class="healthReportDetails">                                                                                                                                   |                                                     | 14202'
    '440 | 14203 | <table border="0">                                                                                                                                                  |                                                     | 14220'
    '441 | 14221 | <thead>                                                                                                                                                             |                                                     | 14227'
    '442 | 14228 | <tr>                                                                                                                                                                |                                                     | 14231'
    '443 | 14232 | <th align="left">                                                                                                                                                   | W                                                   | 14248'
    '444 | 14250 | </th>                                                                                                                                                               |                                                     | 14254'
    '445 | 14255 | <th align="left">                                                                                                                                                   | Description                                         | 14271'
    '446 | 14283 | </th>                                                                                                                                                               |                                                     | 14287'
    '447 | 14288 | <th align="right">                                                                                                                                                  | %                                                   | 14305'
    '448 | 14307 | </th>                                                                                                                                                               |                                                     | 14311'
    '449 | 14312 | </tr>                                                                                                                                                               |                                                     | 14316'
    '450 | 14317 | </thead>                                                                                                                                                            |                                                     | 14324'
    '451 | 14325 | <tbody>                                                                                                                                                             |                                                     | 14331'
    '452 | 14332 | <tr>                                                                                                                                                                |                                                     | 14335'
    '453 | 14336 | <td align="left">                                                                                                                                                   |                                                     | 14352'
    '454 | 14353 | <svg viewBox="0 0 24 24" focusable="false" class="svg-icon icon-health-40to59 icon-sm">                                                                             |                                                     | 14439'
    '455 | 14440 | <use href="/static/e774c451/images/build-status/weather-sprite.svg#weather-cloudy">                                                                                 |                                                     | 14522'
    '456 | 14523 | </use>                                                                                                                                                              |                                                     | 14528'
    '457 | 14529 | </svg>                                                                                                                                                              |                                                     | 14534'
    '458 | 14535 | </td>                                                                                                                                                               |                                                     | 14539'
    '459 | 14540 | <td>                                                                                                                                                                | Build stability: 2 out of the last 5 builds failed. | 14543'
    '460 | 14595 | </td>                                                                                                                                                               |                                                     | 14599'
    '461 | 14600 | <td align="right">                                                                                                                                                  | 60                                                  | 14617'
    '462 | 14620 | </td>                                                                                                                                                               |                                                     | 14624'
    '463 | 14625 | </tr>                                                                                                                                                               |                                                     | 14629'
    '464 | 14630 | </tbody>                                                                                                                                                            |                                                     | 14637'
    '465 | 14638 | </table>                                                                                                                                                            |                                                     | 14645'
    """
    @classmethod
    def from_text(cls, text, token_start='<', token_end='>'):
        """
        #>>> et = ElementTable.from_text(data.text_from('JENKINS_ROOT.htm'))
        #>>> len(list(et.row_gen()))
        2731
        """
        ht = cls()
        row = -1
        ht.set_val(row, 'beg', 0)
        ht.set_val(row, 'tag', '')
        for token_ndx in range(len(text)):
            tag = ht.get_val(row, 'tag')
            token = text[token_ndx]
            bucket = 'tag'
            if token == token_start:
                if tag and not tag.endswith(token_end):
                    print("THIS SHOULD NOT HAPPEN?")
                new_value = ht.get_val(row, 'tag_value', '')
                new_value = ' '.join(new_value.split())
                ht.set_val(row, 'tag_value', new_value)
                row += 1
                ht.set_val(row, 'beg', token_ndx)
            elif token == token_end:
                if not tag.endswith(token_end):
                    ht.set_val(row, 'end', token_ndx)
                else:
                    ended_already = ht.get_val(row, 'ended_already', [])
                    ended_already.append(token_ndx)
                    ht.set_val(row, 'ended_already', ended_already)
            else:
                if row == -1 or tag is not None and tag.endswith(token_end):
                    bucket = 'tag_value'

            old_val = ht.get_val(row, bucket, '')
            ht.set_val(row, bucket, old_val + token)
        return ht


class TableTable(table.Table):

    @classmethod
    def from_text_gen(cls, text):
        """
        See token 398 below is the third table from the top and contains subtables (depth 2) for id="projectstatus"
        #>>> TableTable.from_text(data.text_from('JENKINS_ROOT.htm'))
        1 227 <table class="pane ">
        0 234 </table>
        1 255 <table class="pane ">
        0 339 </table>
        1 398 <table id="projectstatus" class="sortable pane bigtable stripped-odd ">
        2 440 <table border="0">
        1 465 </table>
        2 512 <table border="0">
        1 537 </table>
        2 585 <table border="0">
        1 610 </table>
        2 658 <table border="0">
        1 683 </table>
        2 731 <table border="0">
        1 756 </table>
        2 802 <table border="0">
        1 827 </table>
        2 874 <table border="0">
        1 899 </table>
        2 948 <table border="0">
        1 973 </table>
        2 1022 <table border="0">
        1 1047 </table>
        2 1096 <table border="0">
        1 1121 </table>
        2 1167 <table border="0">
        1 1192 </table>
        2 1235 <table border="0">
        1 1260 </table>
        2 1427 <table border="0">
        1 1452 </table>
        2 1499 <table border="0">
        1 1524 </table>
        2 1573 <table border="0">
        1 1598 </table>
        2 1645 <table border="0">
        1 1670 </table>
        2 1717 <table border="0">
        1 1742 </table>
        2 1790 <table border="0">
        1 1815 </table>
        2 1865 <table border="0">
        1 1890 </table>
        2 1938 <table border="0">
        1 1963 </table>
        2 2013 <table border="0">
        1 2038 </table>
        2 2087 <table border="0">
        1 2112 </table>
        2 2161 <table border="0">
        1 2186 </table>
        2 2233 <table border="0">
        1 2258 </table>
        2 2305 <table border="0">
        1 2330 </table>
        2 2378 <table border="0">
        1 2403 </table>
        2 2453 <table border="0">
        1 2478 </table>
        2 2528 <table border="0">
        1 2553 </table>
        2 2603 <table border="0">
        1 2628 </table>
        0 2652 </table>
        1 2654 <table style="width:100%">
        0 2705 </table>

        The table of tables (id:"projectstatus") ends at element 2652

        """
        et = ElementTable.from_text(text)
        ttq = []
        for et_row in et.row_gen():
            tag = et.get_val(et_row, 'tag')
            tag_value = et.get_val(et_row, 'tag_value')
            if not tag:
                continue
            if tag.startswith('<table'):
                tt = cls((
                    (0, 'beg_tag', tag),
                    (0, 'end_tag', None),
                ))
                ttq.append(tt)
            elif tag.startswith('</table'):
                if not ttq:
                    raise ValueError(f"TABLE END TAG HAS NO MATCHING BEGIN TAG: element row: {et_row}  tag: {tag}")
                tt = ttq[-1]
                tt.set_val(0, 'end_tag', tag)
                yield tt
                ttq = ttq[:-1]
            elif tag.startswith('<tr'):
                if not ttq:
                    continue
                tt = ttq[-1]
                row = tt.length
                tt.set_val(row, 'beg_tag', tag)
                pass
            elif tag.startswith('</tr'):
                if not ttq:
                    continue
                tt = ttq[-1]
                row = tt.length - 1
                tt.set_val(row, 'end_tag', tag)
                pass
            elif tag.startswith('<td'):
                if not ttq:
                    continue
                tt = ttq[-1]
                row = tt.length
                tt.set_val(row, 'beg_tag', tag)
                pass
            elif tag.startswith('</td'):
                if not ttq:
                    continue
                tt = ttq[-1]
                row = tt.length - 1
                tt.set_val(row, 'end_tag', tag)
                pass


            else:
                if not ttq:
                    continue
                tt = ttq[-1]
                tt.append_tag_value(tag, tag_value)

    def append_tag_value(self, tag, value):
        row = self.length - 1
        tag_values = self.get_val(row, 'tag_values', [])
        tag_values.append((tag, value))
        self.set_val(row, 'tag_values', tag_values)


