def hex_to_unicode(hex_code):
    return '\U{0:0>8}'.format(hex_code).decode('unicode-escape')
