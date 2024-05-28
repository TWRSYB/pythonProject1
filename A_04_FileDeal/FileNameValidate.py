import re

list_spc = [
    ('\n', '_SPC01_'),
    ('\t', '_SPC02_'),
    (':', '_SPC03_'),
    ('*', '_SPC04_'),
    ('?', '_SPC05_'),
    ('"', '_SPC06_'),
    ('<', '_SPC07_'),
    ('>', '_SPC08_'),
    ('|', '_SPC09_'),
    ('/', '_SPC10_'),
    ('\\', '_SPC11_'),
]

def validate(file_name_str):
    print(file_name_str)
    r_str = r"[\/\\\:\*\?\"\<\>\|\n\t]"
    file_name_str = re.sub(r_str, "_SPC_", file_name_str)
    print(file_name_str)
    return file_name_str


def correct_name(file_name_str: str, can_restored=False):
    if not can_restored:
        r_str = r"[\/\\\:\*\?\"\<\>\|\n\t]"
        file_name_str = re.sub(r_str, '', file_name_str)
        return file_name_str
    else:
        for spc in list_spc:
            file_name_str = file_name_str.replace(spc[0], spc[1])
        return file_name_str


if __name__ == '__main__':
    s = '[父女乱伦】 禽兽父亲给女儿\t玩平板，  借机插         入内射浓浓:\n::?精液'
    print(s)
    validate1 = correct_name(s, True)
    print(validate1)
