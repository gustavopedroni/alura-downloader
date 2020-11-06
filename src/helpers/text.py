def file_folder_name(t):

    return t.replace(':', f' -') \
            .replace('/', ' ') \
            .replace('\\', ' ') \
            .replace('?', '.') \
            .replace('"', "'") \
            .replace('<', ' ') \
            .replace('>', ' ') \
            .replace('|', '-')
