# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : zero_width_string.py
@Project  : MyProject
@Time     : 2023/11/20 15:05
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     :  
@Last Modify Time          @Version        @Author
--------------------       --------        -----------
2023/11/20 15:05            1.0             Zhang ZiXu
"""
import re


def remove_zero_width_chars(text):
    """
    Remove zero width characters from the given text.

    :param text: The input string that may contain zero width characters.
    :return: A string with zero width characters removed.
    """
    zero_width_pattern = r'[\u200B-\u200F\u202A-\u202E]'
    return re.sub(zero_width_pattern, '', text)


# 示例使用
example_text = r"\u200e\u200e85"
cleaned_text = remove_zero_width_chars(example_text)
print("Original:", example_text)
print("Cleaned:", cleaned_text)

import re


def extract_numbers(text, default):
    """
    使用正则表达式匹配数字。

    Args:
        text: 传入文本。
        default: 如果没有找到匹配项时的默认值。

    Returns:
        匹配到的数字或默认值。
    """
    pattern = r'[\d]+'
    numbers = re.search(pattern, text)
    return numbers.group() if numbers else default


# 示例使用
# example_text = '68\u200f\u200f\u200f\u200f\u200f\u200f\u200f\u200f\u200f'
example_text = '1\xa0214'
extracted_numbers = extract_numbers(example_text, "")
print(f"{type(extracted_numbers)}:", extracted_numbers)
