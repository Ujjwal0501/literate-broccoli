#!/usr/bin/env python

from os import listdir
from os.path import isfile, join
from pathlib import Path
from io import BytesIO, StringIO
import svg_stack as ss
import numpy as np
import math, shutil


COLUMN_HEIGHT = 10
ROW_SIZE = 10
PAGE_SIZE = COLUMN_HEIGHT * ROW_SIZE


def gen_page(file_name, page):
    doc = ss.Document()
    vertical_layout = ss.HBoxLayout()

    for row in page:
        content = False
        horizontal_layout = ss.VBoxLayout()
        for item in row:
            if not item or item == '\n' or item == "":
                continue
            horizontal_layout.addSVG('./out/'+item,alignment=ss.AlignTop|ss.AlignHCenter)
            content = True
        if content:
            vertical_layout.addLayout(horizontal_layout)
        
    doc.setLayout(vertical_layout)
    doc.save(file_name)


def gen_page_inm(file_name, page):
    doc = ss.Document()
    vertical_layout = ss.HBoxLayout()

    for row in page:
        content = False
        horizontal_layout = ss.VBoxLayout()
        for item in row:
            if not isinstance(item, BytesIO):
                continue
            horizontal_layout.addSVG(item,alignment=ss.AlignTop|ss.AlignHCenter)
            content = True

        if content:
            vertical_layout.addLayout(horizontal_layout)
        
    doc.setLayout(vertical_layout)
    doc.save(file_name)

    # close all in-memory individual SVGs
    [[ele.close() if isinstance(ele, BytesIO) else None for ele in row] for row in page]



def page_svg_from_svg_list(svg_list, column_num=COLUMN_HEIGHT, row_num=ROW_SIZE):
    entry_count = column_num * row_num
    page_count = math.ceil(len(svg_list) / entry_count)
    pages = np.array(svg_list)
    pages_s = [StringIO() for i in range(page_count)]

    pages.resize((page_count, column_num, row_num))
    [gen_page_inm(pages_s[idx], page) for idx, page in enumerate(pages)]
    
    return pages_s



if __name__ == "__main__":
    # called from terminal

    shutil.rmtree("out-pages", ignore_errors=True)

    Path("out-pages").mkdir(parents=True, exist_ok=True)
    pages = [f for f in listdir("out") if isfile(join("out", f))]
    pages.sort(key=lambda x:int(x.split('-')[0]))

    pages = np.array(pages)
    pages.resize((math.ceil(len(pages) / PAGE_SIZE), COLUMN_HEIGHT, ROW_SIZE))
    [gen_page('out-pages/page_' + str(num) + '.svg', page) for num, page in enumerate(pages, start=1)]
