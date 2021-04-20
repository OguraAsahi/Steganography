from jpegEncode import encode
from analyze import histogramAnalyze

# writer of JSteg
def writeDCT(dct, index, data):
    value = dct[index]
    # 获取二进制存储的AC系数，判断该AC系数是否等于正负1或0，若等于则跳过该AC系数，否则，执行下一步
    if value in (-1, 1, 0):
        return False
    # 判断二进制存储的AC系数的LSB是否与要嵌入的秘密信息比特相同, 通过data - lsb的形式
    lsb = value % 2
    # 如果秘密信息与最低比特位不同，则使用秘密信息值代替最低比特位
    if value > 0:
        dct[index] += data - lsb
    else:
        dct[index] -= data - lsb
    return True


with open("./samples/plain.txt", "rb") as f: # encode and analyze
    histogramAnalyze(encode("./samples/lena.jpg", "./samples/lena_jsteg.jpg", f.read(), writeDCT), "./results/jsteg.png")


# 未经过信息隐藏的DCT系数，系数近似符合拉普拉斯分布，具有几个典型特点
    #对称性 以0为中心达到最大值，两侧分布近似对称
    # 单侧单调性 以0值为中心达到最大值，两侧单调下降
    # 梯度下降性 小值样点较多，大值样点较少，分布曲线在两侧下降梯度逐渐减小
    
# JSteg隐写可嵌入信息的DCT系数较少，隐写量较小，且相邻数值样点的个数接近，如2和3，-2和-3形成了值对，卡方特征变化明显，因而提出了F3隐写