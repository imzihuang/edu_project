#coding:utf-8


def reg_sub_ex(reg_ob, s, mcb):
    """
    增强型正则替换
    
    :param reg_ob: regex object
    :param s: input string
    :param mcb: match to str callback
    """
    assert mcb and callable(mcb)

    ms = tuple(reg_ob.finditer(s))
    if not ms:
        return s

    rt = []
    for i in xrange(len(ms)):
        unmatch = s[0: ms[i].start()] if 0 == i else s[ms[i - 1].end(): ms[i].start()]

        rt.append(unmatch)
        rt.append(mcb(ms[i]))

    rt.append(s[ms[-1].end():])
    return ''.join(rt)