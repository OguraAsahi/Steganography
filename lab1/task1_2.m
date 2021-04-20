Picture=imread('stego.bmp');
Picture=double(Picture);
[m,n]=size(Picture);

frr=fopen('message.txt','a');
len=80;
p=1;
for f2=1:n
    for f1=1:m
        %按照产生的随机数序列依次读取图像的相应点最后一位的信息。并将其以二进制形式写到文件中
        %fwrite函数的作用是将内存中的二进制数据原样写入文件中
        %是ubit后面的数字表示是一次读几位，中间的数据表示读几次
        if bitand(Picture(f1,f2),1)==1  %按位与运算
            fwrite(frr,1,'ubit1');
            result(p,1)=1;
        else
            fwrite(frr,0,'ubit1');
            result(p,1)=0;
        end
        if p==len
            break;
        end
        if p<len
            p=p+1;
        end
    end
    if p==len
        break;
    end
end
fclose(frr);