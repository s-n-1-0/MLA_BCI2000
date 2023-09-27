% %MATLABで被験者内一要因の分散分析をおこなう
% (例題mtrx.mの中身は96*9の観測データが存在する)

%%load mtrx.mat
mtrx = readtable("C:\MLA_Saves_Bk\evals\acc_results.csv");
mtrx = table2array(mtrx(:, 1:end));

group = ones(size(mtrx,1),1);%被験者内要因は1つしかないので全て1
args = {};
tsize = 4;
names = {'G'};
for i = 1:tsize
    names{end+1} = ['t',num2str(i)];
end
t = table(group, ...
          mtrx(:,1),mtrx(:,2),mtrx(:,3),mtrx(:,4),...#,mtrx(:,5),mtrx(:,6),mtrx(:,7),mtrx(:,8), ...
          'VariableNames',names);

Meas = table([1:tsize].','VariableNames',{'Time'});

rm = fitrm(t,['t1-t',num2str(tsize),'~G-1'],'WithinDesign',Meas);
% 重要 : G-1によってcortisolの要因を抜くことができる
% Groupが複数ある(混合計画)の場合にはGの中の値が複数になる
ranovatbl = ranova(rm);
