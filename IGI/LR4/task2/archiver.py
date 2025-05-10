import zipfile
from datetime import datetime

def create_archive(file_path, archive_name):
    try:
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(file_path)
        print(f"Created archive: {archive_name}")
    except Exception as e:
        print(f"Error creating archive: {e}")

def display_archive_info(archive_name):
    try:
        with zipfile.ZipFile(archive_name, 'r') as zf:
            print(f"Archive: {archive_name}")
            for info in zf.infolist():
                print(f"  File: {info.filename}")
                mod_time = datetime(*info.date_time)
                print(f"    Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"    Size: {info.file_size} bytes")
                print(f"    Compressed: {info.compress_size} bytes")
                print(f"    Compression: {zf.compression}")
    except Exception as e:
        print(f"Error reading archive: {e}")