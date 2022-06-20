

def recursive_compare(d1: dict, d2: dict, level: str = 'root') -> str:
    ret = []
    if isinstance(d1, dict) and isinstance(d2, dict):
        if d1.keys() != d2.keys():
            s1 = set(d1.keys())
            s2 = set(d2.keys())
            ret.append('{:<20} - {} + {}'.format(level, ','.join(s1 - s2), ','.join(s2 - s1)))
            common_keys = s1 & s2
        else:
            common_keys = set(d1.keys())

        for k in common_keys:
            ret.append(recursive_compare(d1[k], d2[k], level='{}.{}'.format(level, k)))
    elif isinstance(d1, list) and isinstance(d2, list):
        if len(d1) != len(d2):
            ret.append('{:<20} len1={}; len2={}'.format(level, len(d1), len(d2)))
        common_len = min(len(d1), len(d2))

        for i in range(common_len):
            ret.append(recursive_compare(d1[i], d2[i], level='{}[{}]'.format(level, i)))
    else:
        if d1 != d2:
            ret.append('{:<20} {} -> {}'.format(level, d1, d2))
    return '\n'.join(filter(None, ret))