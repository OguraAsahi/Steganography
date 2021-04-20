# Steganography

# 空域编码图像
* 空域编码是指在图像空间域进行编码，也就是直接针对图像像素进行编码
* 对像素进行编码，如LSB算法，主要有下面两种方式
   * 光栅格式
   * 调色板格式   GIF(graphics interchange format)
* 一个图像编码标准往往包括多类编码方法，一个图像仅仅是其一类方法的实例。例如，常见的BMP（Bitmap）、 TIFF（
Tagged Image File Format）、 PNG（Portable Network
Graphics）均支持光栅格式与调色板格式编码，对这两种格式
编码分别又支持多种具体编码方法
## LSB隐写算法
* LSB隐写是最基础、最简单的隐写方法，具有容量大、嵌入速度快、对载体图像质量影响小的特点

* LSB的大意就是最低比特位隐写。我们将深度为8的BMP图像，分为8个二值平面（位平面），我们将待嵌入的信息（info）直接写到最低的位平面上。换句话说，如果秘密信息与最低比特位相同，则不改动；如果秘密信息与最低比特位不同，则使用秘密信息值代替最低比特位


# 变换域编码图像

### JSteg隐写
* JSteg的算法的主要思想是将秘密消息嵌入在量化后的DCT系数的最低比特位上，但对原始值为0、+1、-1的DCT系数不进行嵌入，提取秘密消息时，只需将载密图像中不等于0、l的量化DCT系数的LSB取出即可
* JSteg算法步骤 

1. 选择载体图像，并且将载体图像划分为连续的8×8的子块。 
2. 对每个子块使用离散余弦变换之后，用相应的质量因数的量化表量化，得到对应的8×8量化DCT子块。 
3. 将需要隐藏的信息编码为二进制数据流，对DCT子块系数进行Z字形扫描，并且使用秘密信息的二进制流替换非0和非1的DCT系数的最低比特位。 
4. 进行熵编码等，产生JPEG隐密图像。

* JSteg的具体嵌入过程
1. 部分解码JPEG图像，得到二进制存储的AC系数，判断该AC系数是否等于正负1或0，若等于则跳过该AC系数，否则，执行下一步
2. 判断二进制存储的AC系数的LSB是否与要嵌入的秘密信息比特相同，若相同，则不对其进行修改，否则执行下一步
3. 用秘密信息比特替换二进制存储的AC系数的LSB，将修改后的AC系数重新编码得到隐秘JPEG图像
* JSteg不使用0、1的原因
1. DCT系数中“0”的比例最大（一般可达到60%以上，取决于图像质量和压缩因子），压缩编码是利用大量出现连零实现的，如果改变DCT系数中“0”的话，不能很好的实现压缩
2. DCT系数中的“1”若变成“0”，由于接受端无法区分未使用的“0”和嵌入消息后得到的“0”，从而无法实现秘密信息的提取

### F3隐写
* 为了改善大量DCT系数不隐藏信息这一状况，人们提出了F3隐写
* F3对原始值为+1和-1的DCT系数，进行了利用。F3隐写的规则如下

1. 每个非0的DCT数据用于隐藏1比特秘密信息，为0的DCT系数不负载秘密信息
2. 如果秘密信息与DCT的LSB相同，便不作改动；如果不同，将DCT系数的绝对值减小1，符号不变
3. 当原始值为+1或-1且预嵌入秘密信息为0时，将这个位置归0并视为无效，在下一个DCT系数上重新嵌入

* 编写代码实现嵌入，并观察DCT系数变化
```
JPEG的DCT系数
{0: 32939, 1: 15730, 2: 13427, 3: 11523, 4: 9540, 5: 7957, 6: 6607, 7: 5697, 8: 4834, -1: 15294, -2: 13637, -3: 11479, -4: 9683, -5: 7979, -6: 6878, -7: 5631, -8: 4871}
Jsteg begin writing!
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
经过信息隐藏后JPEG的DCT系数变化
{0: 32939, 1: 15730, 2: 12552, 3: 12398, 4: 8739, 5: 8758, 6: 6165, 7: 6139, 8: 4487, -1: 15294, -2: 12721, -3: 12395, -4: 8891, -5: 8771, -6: 6319, -7: 6190, -8: 4463}
F3steg begin writing!
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
经过信息隐藏后JPEG的DCT系数变化
{0: 47068, 1: 13416, 2: 13519, 3: 10075, 4: 9545, 5: 7077, 6: 6650, 7: 5016, 8: 4754, -1: 13308, -2: 13668, -3: 10124, -4: 9571, -5: 7249, -6: 6591, -7: 5098, -8: 4733}
F4steg begin writing!
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
经过信息隐藏后JPEG的DCT系数变化
{0: 59320, 1: 13618, 2: 11987, 3: 9875, 4: 8328, 5: 6860, 6: 5883, 7: 4910, 8: 4239, -1: 13692, -2: 11976, -3: 9976, -4: 8428, -5: 7007, -6: 5834, -7: 4964, -8: 4190}
```
* 条形图绘制

![Image text](https://raw.githubusercontent.com/librauee/Staganalysis/master/picture/original.png#pic_center) 
* 未经过信息隐藏的DCT系数，系数近似符合拉普拉斯分布，具有几个典型特点
   * 对称性 以0为中心达到最大值，两侧分布近似对称
   * 单侧单调性 以0值为中心达到最大值，两侧单调下降
   * 梯度下降性 小值样点较多，大值样点较少，分布曲线在两侧下降梯度逐渐减小
![Image text](https://raw.githubusercontent.com/librauee/Staganalysis/master/picture/Jsteg.png#pic_center) 
* JSteg隐写的DCT系数
  * JSteg隐写可嵌入信息的DCT系数较少，隐写量较小，且相邻数值样点的个数接近，如2和3，-2和-3形成了值对，卡方特征变化明显，因而提出了F3隐写
![Image text](https://raw.githubusercontent.com/librauee/Staganalysis/master/picture/F3.png#pic_center) 
* F3隐写的DCT系数
  * F3的设计虽然防止了相邻值出现数量接近的现象，也维持了分布函数的对称性，但使得偶数的分布增加，没有满足单调性
  * 这是因为载体绝对值为1的数值较多，当其被修改为0时，嵌入算法继续嵌入直到找到一个偶数值，或者将一个奇数值改为偶数值，这样绝对值为1的系数可以支持嵌入1，但是不支持嵌入0，需要使用或制造一个偶数
  * 另外，0系数的数量有相应的增加，产生分布曲线向0收缩的现象

### F4隐写
* 为了克服F3的缺陷，F4对不同正负号的奇偶系数采用了不同的嵌入与消息表示方法
* **F4用负偶数、正奇数代表嵌入了消息比特1，用负奇数、正偶数代表嵌入了0**
* 但仍然通过减小绝对值的方法进行修改，如果减小绝对值后系数为0则继续往下嵌入当前比特 
  ![Image text](https://raw.githubusercontent.com/librauee/Staganalysis/master/picture/F4.png#pic_center) 
* F4隐写的DCT系数
  * F4显然保持了载体分布函数的对称性，也保持了载体分布函数的单调性与梯度下降性
  * 但F4依然存在使含密载体分布函数形状向0收缩的现象

### F5隐写
* F5隐写实现了基于汉明码的矩阵编码隐写，在一个分组上最多修改R=1次以嵌入$2^r-1-r$比特，采用的基本嵌入方法是基于F4隐写的
* F5的嵌入步骤
1. 获得嵌入域。若输入的是位图，则进行JPEG编码得到JPEG系数；若输入的是JPEG图像，则进行熵编码的解码得到JPEG系数

2. 位置置乱。根据口令生成的密钥位一个伪随机数发生器，基于伪随机数发生器置乱JPEG系数的位置

3. 编码参数确定。为了提高嵌入效率，一般希望n尽可能大，因此，根据载体中可用系数的数量与消息的长度确定参数r，并计算$n=2^r-1$ 

4. 基于（$n=2^r-1,r$）的汉明分组码得到编码校验矩阵，开始嵌入消息：①按置乱后的顺序取下面n个非零系数，在其中的LSB序列中按照以上编码嵌入n-r比特的消息；②如果未发生修改，并且还有需要嵌入的消息，则返回①继续嵌入下一分组；③如果进行了修改，则判断是不是有系数值收缩到0，如果没有，并且还有需要嵌入的消息则返回①继续嵌入下一分组，如果有，取出一个新的非零系数组成新的一组n个非零系数，在其中的LSB序列中按照以上编码重新嵌入以上n-r比特的消息，直到没有修改或收缩，最后，如果还有需要嵌入的消息，则返回①继续嵌入下一分组

5. 位置逆置乱。恢复DCT系数原来的位置顺序
6. 熵编码。按照JPEG标准无损压缩DCT量化系数，得到JPEG文件



# 参考资料
* 隐写学原理与技术 By 赵险峰
* 数字媒体中的隐写术 By J.Fridrich