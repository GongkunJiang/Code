clc
close all
% 给图像加噪声

dirs = dir('C:\Users\Dell\Desktop\*.bmp');
dircell = struct2cell(dirs);
for i=1:1
    filename = dircell(i, 1);
    disp(filename);
%     split2 = strsplit(filename, '.');
%     disp('-----split');
%     disp(split2);
    each_dir = strcat('C:\Users\Dell\Desktop\',filename);
    disp(each_dir);
    img = imread(char(each_dir));
    subplot(3,3,1);
    imshow(img);      %显示原始图像
end

% path = 'C:\Users\Dell\Desktop\baboon.bmp';
% img = imread(path);