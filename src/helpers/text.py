def file_folder_name(t, r='-'):
    return t.replace(':', f' {r}').replace('/', r).replace('?', r)
