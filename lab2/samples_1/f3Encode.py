from jpegEncode import encode
from analyze import histogramAnalyze

# Ϊ�˸��ƴ���DCTϵ����������Ϣ��һ״�������������F3��д
# F3��ԭʼֵΪ+1��-1��DCTϵ��������������
# writer of F3
def writeDCT(dct, index, data):
    value = dct[index]
    # ÿ����0��DCT������������1����������Ϣ��Ϊ0��DCTϵ��������������Ϣ
    if value == 0:
        return False
    # ��ԭʼֵΪ+1��-1��ԤǶ��������ϢΪ0ʱ�������λ�ù�0����Ϊ��Ч������һ��DCTϵ��������Ƕ��
    if value in (-1, 1) and data == 0:
        dct[index] = 0
        return False

    lsb = value % 2

    # ���������Ϣ��DCT��LSB��ͬ���㲻���Ķ��������ͬ����DCTϵ���ľ���ֵ��С1�����Ų���
    if lsb != data:
        if value > 0:
            dct[index] -= 1
        else:
            dct[index] += 1
    return True


with open("./samples/plain.txt", "rb") as f: # encode and analyze
    histogramAnalyze(encode("./samples/lena.jpg", "./samples/lena_f3.jpg", f.read(), writeDCT), "./results/f3.png")

# F3�������Ȼ��ֹ������ֵ���������ӽ�������Ҳά���˷ֲ������ĶԳ��ԣ���ʹ��ż���ķֲ����ӣ�û�����㵥����
# ������Ϊ�������ֵΪ1����ֵ�϶࣬���䱻�޸�Ϊ0ʱ��Ƕ���㷨����Ƕ��ֱ���ҵ�һ��ż��ֵ��
# ���߽�һ������ֵ��Ϊż��ֵ����������ֵΪ1��ϵ������֧��Ƕ��1�����ǲ�֧��Ƕ��0����Ҫʹ�û�����һ��ż��
# ���⣬0ϵ������������Ӧ�����ӣ������ֲ�������0����������