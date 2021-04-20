from jpegEncode import encode
from analyze import histogramAnalyze

# 为了改善大量DCT系数不隐藏信息这一状况，人们提出了F3隐写
# F3对原始值为+1和-1的DCT系数，进行了利用
# writer of F3
def writeDCT(dct, index, data):
    value = dct[index]
    # 每个非0的DCT数据用于隐藏1比特秘密信息，为0的DCT系数不负载秘密信息
    if value == 0:
        return False
    # 当原始值为+1或-1且预嵌入秘密信息为0时，将这个位置归0并视为无效，在下一个DCT系数上重新嵌入
    if value in (-1, 1) and data == 0:
        dct[index] = 0
        return False

    lsb = value % 2

    # 如果秘密信息与DCT的LSB相同，便不作改动；如果不同，将DCT系数的绝对值减小1，符号不变
    if lsb != data:
        if value > 0:
            dct[index] -= 1
        else:
            dct[index] += 1
    return True


with open("./samples/plain.txt", "rb") as f: # encode and analyze
    histogramAnalyze(encode("./samples/lena.jpg", "./samples/lena_f3.jpg", f.read(), writeDCT), "./results/f3.png")

# F3的设计虽然防止了相邻值出现数量接近的现象，也维持了分布函数的对称性，但使得偶数的分布增加，没有满足单调性
# 这是因为载体绝对值为1的数值较多，当其被修改为0时，嵌入算法继续嵌入直到找到一个偶数值，
# 或者将一个奇数值改为偶数值，这样绝对值为1的系数可以支持嵌入1，但是不支持嵌入0，需要使用或制造一个偶数
# 另外，0系数的数量有相应的增加，产生分布曲线向0收缩的现象