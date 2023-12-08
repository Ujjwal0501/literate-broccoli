
import zipfile
from io import BytesIO, StringIO



def zip_list_of_contents(suffix, content_list):
    in_memory_zip = BytesIO()
    with zipfile.ZipFile(in_memory_zip, 'w', compression=zipfile.ZIP_DEFLATED) as output:
        for idx, item in enumerate(content_list):
            if not isinstance(item, StringIO) and not isinstance(item, BytesIO):
                continue
            output.writestr(f'{suffix}_{idx}.svg', item.getvalue())
            item.close()

    in_memory_zip.seek(0)
    return in_memory_zip