function two_DDR_list = Calculate_2DDR(coord_seq)
%CALCULATE 2DDR for FPHA
%   coord_seq: 50 * 63
%   two_DDR_list: 49 * (25 * 2)

% 25 units
joint_structure = [
    % palm
    2 1 3; 2 1 4; 2 1 5; 2 1 6; 3 1 4; 3 1 5; 3 1 6; 4 1 5; 4 1 6; 5 1 6;
    % thumb
    1 2 7; 2 7 8; 7 8 9;
    % forefinger
    1 3 10; 3 10 11; 10 11 12;
    % middle finger
    1 4 13; 4 13 14; 13 14 15;
    % ring finger
    1 5 16; 5 16 17; 16 17 18;
    % pinky
    1 6 19; 6 19 20; 19 20 21;
];

two_DDR_list = zeros(49, 50);
two_DDR_feature = zeros(49, 2, 25);

% split the sequence into 50 poses
for i = 2: 50
    prev_pose = coord_seq(i - 1, :)
    curr_pose = coord_seq(i, :);
    % split all x,y,z, 1 * 63 -> 3 * 21
    rp_pose = zeros(3, 21);
    rc_pose = zeros(3, 21);
    for j = 1 : 21
        rp_pose(1, j) = prev_pose((j - 1) * 3 + 1);
        rp_pose(2, j) = prev_pose((j - 1) * 3 + 2);
        rp_pose(3, j) = prev_pose((j - 1) * 3 + 3);
        rc_pose(1, j) = curr_pose((j - 1) * 3 + 1);
        rc_pose(2, j) = curr_pose((j - 1) * 3 + 2);
        rc_pose(3, j) = curr_pose((j - 1) * 3 + 3);
    end
    rotation_feature = Calculate_joint_rotation(rp_pose, rc_pose, joint_structure);
    two_DDR_feature(i - 1, :, :) = rotation_feature;
end
for j = 1: 25
    two_DDR_list(:, j * 2 - 1) = two_DDR_feature(:, 1, j);
    two_DDR_list(:, j * 2) = two_DDR_feature(:, 2, j);
end

end

