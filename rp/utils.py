def encoding_sucks(text):
    try:
        return text.encode("Utf-8")
    except UnicodeError:
        pass
    try:
        return text.decode("Utf-8")
    except UnicodeDecodeError:
        pass
    try:
        return text.encode("iso-8859-1")
    except:
        pass
    try:
        return text.decode("iso-8859-1")
    except:
        pass
    return "could not get the title :(, tell Bram that this website sucks"
