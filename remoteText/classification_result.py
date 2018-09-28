# 函数目的：将正则表达式分类结果和算法分类结果进行综合，得出一个最终结果


def fusions(classre,classml):
    """
    :param classre: 正则表达式的分类结果
    :param classml: 算法的分类结果
    :return: 两者综合的分类结果
    """
    classml = list(classml)
    classre = list(classre)
    if len(classre) == 1:     # 如果正则分类结果是一个，则返回正则结果
        return classre[0]
    elif len(classre) < 1:  # 如果正则分类结果为0，则取模型分类结果
        return classml[0]
    elif len(classre) > 1:  # 如果正则分类结果大于1个，则判断这两个分类是否有重合
                            # 有重合取重合，没有重合取正则结果
        a = 0
        try:
            a = classre.index(classml[0])
        except ValueError as e:
            print(e)
        finally:
            return classre[a]



