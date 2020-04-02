close all;clc,clear
box on
hold on
grid on
N=64;
xlabel('\mu');
ylabel('x_n');
title([' N=',num2str(N)]);
set(gca, 'FontSize', 15);
set(gca,'XLim',[0 4]);
set(gca,'YLim',[0 1]);
set(gca, 'XTick',0:1:4);
set(gca, 'YTick',0:0.2:1);
x0=rand(1);e=0.1;xn=zeros(1);yn=zeros(1);count=1;
for k = 0.004:0.004:4
    for b = 1:1000
        x0 =PLM(N,k,x0);
        if b > 1000-64
            xn(count)=x0;
            count=count+1;
        end
    end
end

for n = 1:1000
    if n == 1
        yn(n)=xn(n);
    else
        yn(n)=(1-e)*xn((n-1)*64+1)+(e/4)*(xn((n-1)*64+2)+xn((n-1)*64+8)+xn((n-1)*64+9)+xn((n-1)*64+57));
    end
    plot(n/250,yn(n),'ob');
end


function y=PLM(N,k,x0)
    if x0>0&&x0<1/N
        y = k.*N^2.*x0.*(1/N-x0);       
    elseif x0>1/N&&x0<1
        for j=1:2:(N-1)
            if x0>j/N&&x0<(j+1)/N
                y=1-k.*N^2.*(x0-j/N).*((j+1)/N-x0);
            end
        end
        for j=2:2:(N-1)
            if x0>j/N&&x0<(j+1)/N
                y=k.*N^2.*(x0-j/N)*((j+1)/N-x0);                
            end
        end
    elseif x0==1
        y=x0-1/(100*N);        
    else
        y=x0+1/(100*N);      
    end
end


%saveas(gcf,['images/img10_N',num2str(N)],'png');







