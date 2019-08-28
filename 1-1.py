def get_max_index(array, unlimit=None):
    """
    获取字符串中每个字符最大索引字典
    :param array: 小写字母字符串
    :param unlimit: 非限制字母表
    :return: 每个字符最大索引字典
    """
    max_index_dict = {}
    character_list = set(array)

    length_of_array = len(array)
    re_array = array[::-1]
    for c in character_list:
        i = re_array.index(c)
        max_index_dict[c] = length_of_array-i-1

    if unlimit is not None:
        for x in unlimit:
            max_index_dict[x] = -1

    return max_index_dict


def get_all_part_set(array, max_index_dict):
    """
    按最大索引表将序列拆分成多个序列，任意两个序列之间没有交集
    :param array: 序列字符串
    :param max_index_dict: 最大索引表
    :return: 子序列表
    """
    part_list = []
    index_list = [0]
    max = -1

    for i, c in enumerate(array):
        if max_index_dict[c] > max:
            max = max_index_dict[c]
        elif i == max:
            max = i+1
            index_list.append(i+1)

    for i in range(len(index_list)-1):
        part_list.append(array[index_list[i]:index_list[i+1]])

    return part_list


if __name__ == '__main__':

    array = input("请输入序列\n")
    max_index_dict = get_max_index(array, ['a'])
    part_set = get_all_part_set(array, max_index_dict)
    for x in part_set:
        print(x)
