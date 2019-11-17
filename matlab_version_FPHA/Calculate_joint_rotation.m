function joint_rotation_feature = Calculate_joint_rotation(data_prev, data_curr, joint_structure)
%CALCULATE_JOINT_ROTATION 
%   included_angle_diff and norm_vec_rotation

joint_rotation_feature = zeros(2, length(joint_structure));

for i = 1: length(joint_structure)
    joint_unit = joint_structure(i, :);
    [included_angle_prev, norm_vec_prev] = Calculate_rotation_status(data_prev, joint_unit);
    [included_angle_curr, norm_vec_curr] = Calculate_rotation_status(data_curr, joint_unit);
    
    included_angle_diff = included_angle_curr - included_angle_prev;
    norm_vec_rotation = Calculate_included_angle(norm_vec_prev, norm_vec_curr);
    
    joint_rotation_feature(1, i) = included_angle_diff;
    joint_rotation_feature(2, i) = norm_vec_rotation;
end

end

