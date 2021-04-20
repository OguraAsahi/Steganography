STEGO='stego5.jpg';
SEED=99;
mlen=80;
k=5;
tic;
messageste=nsf5_extract(STEGO,SEED,mlen,k);
T=toc;

fprintf('-----\n');
fprintf('nsF5 extract finfished\n');
fprintf('elapsed time: %.4f seconds\n',T);
fprintf('message: ');fprintf('%i',messageste);fprintf('\n');

function message=nsf5_extract(STEGO,SEED,mlen,k)
    try
        jobj=jpeg_read(STEGO);
        DCT=jobj.coef_arrays{1};
    catch
        error('ERROR (problem with the STEGO image)');
    end

    AC=numel(DCT)-numel(DCT(1:8:end,1:8:end));
    changeable=true(size(DCT));
    changeable(1:8:end,1:8:end)=false;
    changeable=find(changeable);
    rand('state',SEED);
    changeable=changeable(randperm(AC));
    frr=fopen('message5.txt','a');
    idD=1;
    id=0;
    while(id<mlen)
        if (mlen-id < k)
            k=mlen-id;
        end
        n=2^k-1;
        a=[];
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
        for j=1:k
            res=0;
            for i=1:n
                res=xor(res,bitget(i,j)*mod(DCT(changeable(a(i))),2));
            end
            message(1,id+j)=res;
            if res==1
            fwrite(frr,1,'ubit1');
        else
            fwrite(frr,0,'ubit1');
        end
        end
        id=id+k;
    end  
    fclose(frr);
end