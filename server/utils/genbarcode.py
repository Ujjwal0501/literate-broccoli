import csv, os, shutil
from pathlib import Path
from io import BytesIO
import barcode
from barcode.writer import SVGWriter
from barcode import Code128


# create a custom writer to remove the background element
class CustomWriter(SVGWriter):
    def __init__(self) -> None:
        SVGWriter.__init__(self)
    
    def _init(self, code):
        super()._init(code)
        self._group.removeChild(self._group.lastChild)


def create_barcode_svg(item_list, disk_write=False):
    svg_list = []
    for idx, item in enumerate(item_list):

        # Generate Barcode
        if disk_write:
            fd = open('out/' + item + ".svg", "wb")
        else:
            fd = BytesIO()
            svg_list.append(fd)
        
        Code128(str(item), writer=CustomWriter()).write(fd, options={"module_width": 0.25, "module_height": 8, "margin_top": 3, "margin_bottom": 0, "font_size": 5, "text_distance": 1.55, "quiet_zone": 3})

        if not disk_write:
            fd.flush()
            fd.seek(0)
    return None if disk_write else svg_list



if __name__ == "__main__":
    # called from terminal

    shutil.rmtree("out", ignore_errors=True)
    Path("out").mkdir(parents=True, exist_ok=True)

    with open("tracker.csv") as f:
        list2 = [row.split(",") for row in f]
        for listitem in list2:
            create_barcode_svg(listitem, disk_write=True)