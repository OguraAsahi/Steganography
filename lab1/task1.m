Picture=imread('cover.bmp');
Double_Picture=Picture;
Double_Picture=double(Double_Picture);

%以二进制形式读取要嵌入到图片里的消息。并读取消息的长度（嵌入消息的长度不能超过图像位数）
wen.txt_id=fopen('wen.txt','r');
[msg,len]=fread(wen.txt_id,'ubit1');

[m,n]=size(Double_Picture);
p=1;
for f2=1:n
    for f1=1:m
        %将图片层的最后一位改为消息的信息。即用消息替换图片的最后一位信息。
        %最后一位对图片的影响最小，几乎是肉眼无法识别的。如果是最高位，那么图片就会发生明显的改变
        Double_Picture(f1,f2)=Double_Picture(f1,f2)-mod(Double_Picture(f1,f2),2)+msg(p,1);
        if p==len
            break;
        end
        p=p+1;
    end
    if p==len
        break;
    end
end
%还原图像，就是把嵌入隐藏信息的红层赋值给原图像的红层
Double_Picture=uint8(Double_Picture);
imwrite(Double_Picture,'stego.bmp');
%输出隐藏信息的图像
subplot(121);imshow(Picture);title('未嵌入信息的图像');
subplot(122);imshow(Double_Picture);title('嵌入信息的图像');
fclose(wen.txt_id);