clear;
close all;
clc;
load('sequences_proc.mat', 'sequences_proc');

pose = sequences_proc{1}(1,:);

bones = [
    % palm
    1 2; 1 3; 1 4; 1 5; 1 6;
    % thumb
    2 7; 7 8; 8 9;
    % forefinger
    3 10; 10 11; 11 12;
    % middle finger
    4 13; 13 14; 14 15;
    % ring finger
    5 16; 16 17; 17 18; 
    % pinky
    6 19; 19 20; 20 21;
];

% split all x,y,z, 1 * 63 -> 3 * 21
resized_pose = zeros(3, 21);
for j = 1: 21
    resized_pose(1, j) = pose((j - 1) * 3 + 1);
    resized_pose(2, j) = pose((j - 1) * 3 + 2);
    resized_pose(3, j) = pose((j - 1) * 3 + 3);
end

hold on;
for j = 1: 21
    plot3(resized_pose(1, j), resized_pose(2, j), resized_pose(3, j), '-xb');
    text(resized_pose(1, j), resized_pose(2, j), resized_pose(3, j), num2str(j));
end

for bone = 1 :length(bones)
    start_point = resized_pose(:, bones(bone, 1));
    end_point = resized_pose(:, bones(bone, 2));
    plot_3d_segment(start_point, end_point, '-r');
end
