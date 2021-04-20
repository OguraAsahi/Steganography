from jpegEncode import encode
from analyze import histogramAnalyze

# writer of JSteg
def writeDCT(dct, index, data):
    value = dct[index]
    # ��ȡ�����ƴ洢��ACϵ�����жϸ�ACϵ���Ƿ��������1��0����������������ACϵ��������ִ����һ��
    if value in (-1, 1, 0):
        return False
    # �ж϶����ƴ洢��ACϵ����LSB�Ƿ���ҪǶ���������Ϣ������ͬ, ͨ��data - lsb����ʽ
    lsb = value % 2
    # ���������Ϣ����ͱ���λ��ͬ����ʹ��������Ϣֵ������ͱ���λ
    if value > 0:
        dct[index] += data - lsb
    else:
        dct[index] -= data - lsb
    return True


with open("./samples/plain.txt", "rb") as f: # encode and analyze
    histogramAnalyze(encode("./samples/lena.jpg", "./samples/lena_jsteg.jpg", f.read(), writeDCT), "./results/jsteg.png")


# δ������Ϣ���ص�DCTϵ����ϵ�����Ʒ���������˹�ֲ������м��������ص�
    #�Գ��� ��0Ϊ���Ĵﵽ���ֵ������ֲ����ƶԳ�
    # ���൥���� ��0ֵΪ���Ĵﵽ���ֵ�����൥���½�
    # �ݶ��½��� Сֵ����϶࣬��ֵ������٣��ֲ������������½��ݶ��𽥼�С
    
# JSteg��д��Ƕ����Ϣ��DCTϵ�����٣���д����С����������ֵ����ĸ����ӽ�����2��3��-2��-3�γ���ֵ�ԣ����������仯���ԣ���������F3��д