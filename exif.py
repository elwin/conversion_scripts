import glob
import json
import os
import subprocess
import typing


def main():
    path = "/Users/elwin.stephan/Pictures/fotos-c1/2025 ETH Big Band UK.cocatalog/Originals"

    t5_serial = "4C008763"
    t4_serial = "0BQ13858"
    canon_serial = "6017043"

    files = [f for f in glob.iglob(f"{path}/**/*", recursive=True) if os.path.isfile(f) and (
            f.endswith(".RAF") or
            f.endswith(".raf") or
            f.endswith(".ARW") or
            f.endswith(".awr")
            # f.endswith(".JPG") or
            # f.endswith(".jpg")
    )]

    for file_path in files:
        metadata = get_metadata(file_path)
        serial = metadata.get("SerialNumber")
        if str(serial) != t4_serial:
            continue

        adjust_time_and_offset(
            file_path=file_path,
            time_shift="0:0:0 1:00:00",
            negative=True,
            correct_offset="+01:00",
        )
        print(file_path)


def get_metadata(file_path) -> typing.Dict:
    output = subprocess.check_output(['exiftool', '-json', file_path])
    data = json.loads(output)
    return data[0]


def adjust_time_and_offset(file_path, time_shift, negative, correct_offset):
    sign = "-" if negative else "+"
    subprocess.run([
        "exiftool",
        f"-AllDates{sign}={time_shift}",
        f"-OffsetTimeOriginal={correct_offset}",
        f"-OffsetTime={correct_offset}",
        f"-OffsetTimeDigitized={correct_offset}",
        "-overwrite_original",
        file_path,
    ])

if __name__ == '__main__':
    main()
