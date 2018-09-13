def res(data):
    """
    :param data: 数据塔
    :return: 返回新的数据塔
    """
    for k in range(N):
        dp[N-1].append(data[N-1][k])
    for i in list(range(N-1))[::-1]:
        for j in range(len(data[i+1])-1):
            temp_max = max(dp[i+1][j],dp[i+1][j+1])  # 核心公式
            dp[i].append(temp_max + data[i][j])
    return dp


if __name__ == '__main__':
    data = [[9], [12, 15], [10, 6, 8], [2, 18, 9, 5], [19, 7, 10, 4, 16]]
    dp = [([]) for i in range(len(data))]
    N = len(data)
    dp = res(data)
    print(dp)