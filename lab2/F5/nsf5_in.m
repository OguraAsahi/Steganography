%%% setup
COVER = 'cover.jpg'; % cover image (grayscale JPEG image)
STEGO = 'stego5.jpg'; % resulting stego image that will be created
ALPHA = 0.10; % relative payload in terms of bits per nonzero AC DCT coefficient
SEED = 99; % PRNG seed for the random walk over the coefficients
wen.txt_id=fopen('wen.txt','r') ;
[message ,len] =fread(wen.txt_id,'ubit1');

k=5;
%save('message','message');
tic;
[nzAC] = nsf5_simulation(COVER,STEGO,SEED,message,k,len);
T = toc;

fprintf('-----\n');
fprintf('nsF5 simulation finished\n');
fprintf('cover image: %s\n',COVER);
fprintf('stego image: %s\n',STEGO);
fprintf('PRNG seed: %i\n',SEED);
fprintf('relative payload: %.4f bpac\n',ALPHA);
fprintf('number of nzACs in cover: %i\n',nzAC);
fprintf('elapsed time: %.4f seconds\n',T);
fprintf('message: ');fprintf('%i',message);fprintf('\n');
fclose(wen.txt_id);
function [AC] = nsf5_simulation(COVER,STEGO,SEED,message,k,len)
    %%% load the cover image
    try
        jobj = jpeg_read(COVER); % JPEG image structure
        DCT = jobj.coef_arrays{1}; % DCT plane
    catch
        error('ERROR (problem with the cover image)');
    end
    AC=numel(DCT)-numel(DCT(1:8:end,1:8:end));%非0DCT个数
    if(length(message)>AC)
        error('ERROR(too long message)');
    end
    changeable=true(size(DCT));%创建矩阵
    changeable(1:8:end,1:8:end)=false;%不嵌入DC行为
    changeable=find(changeable);%变化系数指标
    rand('state',SEED);%初始化种子
    changeable=changeable(randperm(AC));%获得随机数
    
    idD=1;
    len=length(message);
    id=0;
    while(id<len)
        if (len-id < k)
            k=len-id;
        end
        Mess=message(id+1:id+k);
        n=2^k-1;
        a=[];
        lastidD=idD;
        for i=1:n
            while(DCT(changeable(idD))==0)
                idD=idD+1;
                if(idD>=AC)
                    break;
                end
            end
            a(i)=idD;
            idD=idD+1;
        end
        C=0;
        for j=1:k
            res=0;
            for i=1:n
                res=xor(res,and(bitget(i,j),mod(DCT(changeable(a(i))),2)));
            end
            if(xor(Mess(j),res)==1)
             	C=bitset(C,j);
            end
        end
        if(C~=0)
            DCT(changeable(a(C)))=DCT(changeable(a(C)))-sign(DCT(changeable(a(C))));
            if(DCT(changeable(a(C)))==0)%结果为0需要重新嵌入
               id=id-k;
               idD=lastidD;
            end
        end
        id=id+k;
    end
    fprintf('idD:%d\n',idD);
    %保存隐写图像
    try
        jobj.coef_arrays{1} = DCT;
        jobj.optimize_coding = 1;
        jpeg_write(jobj,STEGO);
    catch
        error('ERROR (problem with saving the stego image)')
    end
end