def upload_to(file, filename: str):
    file_extension = filename.split('.')[-1]
    creator = file.creator

    return '%s/%s/%s' % (creator, file_extension, filename)
