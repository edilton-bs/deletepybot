"""
Module for looking for code inclusions in text.
"""

from sys import version_info

from ast import PyCF_ONLY_AST as c_flags
if version_info>=(3, 8):
    from ast import PyCF_ALLOW_TOP_LEVEL_AWAIT, PyCF_TYPE_COMMENTS
    c_flags = c_flags | PyCF_ALLOW_TOP_LEVEL_AWAIT | PyCF_TYPE_COMMENTS


def filter_empty_strings(arr:list, indices:list, min_lenght:int) -> list:
    for i, (start, end) in enumerate(indices):
        end = end-1
        while not arr[start]:
            start += 1
        while not arr[end-1]:
            end -= 1
        indices[i] = (start, end)
    return [(start, end) for start, end in indices if (end-start)>=min_lenght]

def find_codeparts(text:str, min_lines=5) -> list:
    """
    Finds a strings of code in the text.
    Returns list of tuples (startline, endline) of line numbers which contains Python code.

    Params: 
        text: str - text to search for code
        min_lines: int - minimum length (in lines) of code inclusions
    """
    code_fragments = []
    lines = text.split('\n')
    start = 0
    end = min_lines
    founded = False
    while end<=len(lines):
        fragment = "\n".join(lines[start:end])
        try:
            compile(fragment, '<string>', 'exec', c_flags)
        except SyntaxError:
            if not founded:
                start += 1
            else:
                code_fragments.append((start, end-1))
                start = end
                founded = False
            end = start+min_lines
        else:
            founded = True
            end += 1
    else:
        if founded:
            code_fragments.append((start, end-1))
    return filter_empty_strings(lines, code_fragments, min_lines)

def get_code_lengths(text:str, min_lines=5)->list:
    """
    Finds a lengths of inclusions of code in text."""
    parts = find_codeparts(text, min_lines)
    return [(end-start) for start, end in parts]
