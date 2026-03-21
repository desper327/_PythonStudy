def factorial(n):
    """n! = n * (n-1)!"""
    if n == 0:          # Base case
        return 1
    return n * factorial(n - 1)  # 递归 + 组合


def sum_list(lst):
    if not lst:               # Base case: 空列表
        return 0
    return lst[0] + sum_list(lst[1:])  # 首元素 + 剩余部分的和


def reverse_list(lst):
    if len(lst) <= 1:
        return lst
    # 最后一个元素 + 反转前面的部分
    return [lst[-1]] + reverse_list(lst[:-1])


