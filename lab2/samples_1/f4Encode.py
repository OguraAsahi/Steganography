from jpegEncode import encode
from analyze import histogramAnalyze

# 为了克服F3的缺陷，F4对不同正负号的奇偶系数采用了不同的嵌入与消息表示方法

# writer of F4
def writeDCT(dct, index, data):
    value = dct[index]
    # 每个非0的DCT数据用于隐藏1比特秘密信息，为0的DCT系数不负载秘密信息
    if value == 0:
        return False
    # 当原始值为+1且预嵌入秘密信息为0时，将这个位置归0并视为无效，在下一个DCT系数上重新嵌入
    if (value == 1 and data == 0) or (value == -1 and data == 1):
        dct[index] = 0
        return False
    lsb = value % 2
    # F4用负偶数、正奇数代表嵌入了消息比特1
    if value > 0 and lsb != data:
        dct[index] -= 1
    # 用负奇数、正偶数代表嵌入了0
    if value < 0 and lsb == data:
        dct[index] += 1
    return True


with open("./samples/plain.txt", "rb") as f: # encode and analyze
    histogramAnalyze(encode("./samples/lena.jpg", "./samples/lena_f4.jpg", f.read(), writeDCT), "./results/f4.png")
    
# F4显然保持了载体分布函数的对称性，也保持了载体分布函数的单调性与梯度下降性
# 但F4依然存在使含密载体分布函数形状向0收缩的现象