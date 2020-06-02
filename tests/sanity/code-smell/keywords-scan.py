#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from flashtext import KeywordProcessor
import sys

def main():
    kw_list=['COPYRIGHT','CONFIDENTIAL','International Business Machine']
    keyword_processor=KeywordProcessor(case_sensitive=False)
    for one_kw in kw_list:
        keyword_processor.add_keyword(one_kw)
    for path in sys.argv[1:] or sys.stdin.read().splitlines():
        with open(path, 'r') as path_fd:
            keywords_found=keyword_processor.extract_keywords(path_fd.read())
            if len(keywords_found) != 0:
                print('%s: %s is found in the file' % (path, keywords_found))
 
if __name__ == '__main__':
    main()