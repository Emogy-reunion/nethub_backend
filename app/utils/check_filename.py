def check_file_extension(filename):
    '''
    checks if the file has an allowed extension
    args:
        filename - the filename to validate
    returns:
        True - if exension is valid
        False - incase of anything else
    '''
    allowed_extensions = ['jpeg', 'jpg', 'png', 'webp']

    if filename and '.' in filename:
        extension = filename.rsplit('.', 1)[1].lower()
    
    if extension in allowed_extensions:
        return True

    return False
