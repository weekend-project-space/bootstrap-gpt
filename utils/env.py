def parse(str):
    array = str.split('\n')
    result = {}
    for line in array:
        if '=' in line:
            kv = line.split('=')
            result[kv[0]] = kv[1]
    return result
