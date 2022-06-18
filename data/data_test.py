#!python3
# encoding=UTF-8
import data
import table


def test_test():
    text = data.text_from('mm17')
    len_text = len(text)
    assert len_text == 25603

    blocks, prompt = data.split_on_prompt(text)
    assert prompt == 'root@mm17:'

    line_counter = 0
    for block in blocks:
        first_line = True
        for line in block.split('\n'):
            line_counter += 1
            if first_line:
                print(line_counter, line)
                first_line = False
