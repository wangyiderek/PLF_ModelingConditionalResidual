A=xlsread('quantilePreSingleISONE CA.csv');
A(:,1)=[];
MAPE=mean(abs(A(:,2)-A(:,1))./A(:,1));
RMSE=sqrt(mean((A(:,2)-A(:,1)).*(A(:,2)-A(:,1))));
MAE=mean(abs(A(:,2)-A(:,1)));
T=length(A(:,1));
Pinball=0;
for i=1:10
    error=A(:,(i+2))-A(:,1);
    Pinball=Pinball+sum(-error(find(error<0))*(i*0.1-0.05))+sum(error(find(error>0))*(1.05-i*0.1));
end
Pinball=Pinball/10/T;
WS=0;
E1=A(:,12)-A(:,1);E2=A(:,3)-A(:,1);
WS=sum(E1-E2)-sum(E1(find(E1<0))*2/0.1)+sum(E2(find(E2>0))*2/0.1);
WS=WS/T;
Result=[MAPE;RMSE;MAE;Pinball;WS]