def print_char (string : str) ->  str :
    mp = {}
    count = 1
    for ch in string :
        mp[ch] = min(mp.get(ch , 0) , count)
        count += 1 
    result : str
    for ch in string :
        for i in range(mp[ch]):
            result += ch
        result += "-"
    result = result[:1]
    print (result)
    return result