def parse(str, splitKey='\n'):
    array = str.split(splitKey)
    result = {}
    for line in array:
        if '=' in line:
            kv = line.split('=')
            result[kv[0]] = kv[1]
        else:
            result[line] = None
    return result
