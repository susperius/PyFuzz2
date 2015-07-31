__author__ = 'susperius'


def split_files(in_file, in_filename):
    pos = in_file.find("-" * 50 + "\r\n")
    if pos == -1:
        return None
    new_file = in_file[pos:]
    in_file = in_file[:pos]
    start_pos = new_file.find("NEW FILE:")
    end_pos = new_file.find("\r\n", start_pos)
    if start_pos == -1 or end_pos == -1:
        return None
    filename = new_file[start_pos:end_pos].split(":")[1]
    start_pos = new_file.find("-" * 50, end_pos)
    start_pos = new_file.find("\r\n", start_pos)
    start_pos += 2
    new_file = new_file[start_pos:]
    return {in_filename: in_file, filename: new_file}


def is_two_files(in_file):
    pos = in_file.find("-" * 50 + "\r\n")
    return True if pos >= 0 else False
