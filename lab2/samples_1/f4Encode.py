from jpegEncode import encode
from analyze import histogramAnalyze

# Ϊ�˿˷�F3��ȱ�ݣ�F4�Բ�ͬ�����ŵ���żϵ�������˲�ͬ��Ƕ������Ϣ��ʾ����

# writer of F4
def writeDCT(dct, index, data):
    value = dct[index]
    # ÿ����0��DCT������������1����������Ϣ��Ϊ0��DCTϵ��������������Ϣ
    if value == 0:
        return False
    # ��ԭʼֵΪ+1��ԤǶ��������ϢΪ0ʱ�������λ�ù�0����Ϊ��Ч������һ��DCTϵ��������Ƕ��
    if (value == 1 and data == 0) or (value == -1 and data == 1):
        dct[index] = 0
        return False
    lsb = value % 2
    # F4�ø�ż��������������Ƕ������Ϣ����1
    if value > 0 and lsb != data:
        dct[index] -= 1
    # �ø���������ż������Ƕ����0
    if value < 0 and lsb == data:
        dct[index] += 1
    return True


with open("./samples/plain.txt", "rb") as f: # encode and analyze
    histogramAnalyze(encode("./samples/lena.jpg", "./samples/lena_f4.jpg", f.read(), writeDCT), "./results/f4.png")
    
# F4��Ȼ����������ֲ������ĶԳ��ԣ�Ҳ����������ֲ������ĵ��������ݶ��½���
# ��F4��Ȼ����ʹ��������ֲ�������״��0����������