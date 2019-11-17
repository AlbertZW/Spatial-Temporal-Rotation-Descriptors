function [included_angle, norm_vec] = Calculate_rotation_status(joint_coords, joint_unit)
%CALCULATE_ROTATION_STATUS 此处显示有关此函数的摘要
%  joint_coords contains all coords of a skeleton
%  joint_unit is the joint indexes of a 2DDR unit

x_temp = joint_coords(1, joint_unit(1));
y_temp = joint_coords(2, joint_unit(1));
z_temp = joint_coords(3, joint_unit(1));
outer_node1 = [x_temp y_temp z_temp];

x_temp = joint_coords(1, joint_unit(2));
y_temp = joint_coords(2, joint_unit(2));
z_temp = joint_coords(3, joint_unit(2));
center_node = [x_temp y_temp z_temp];

x_temp = joint_coords(1, joint_unit(3));
y_temp = joint_coords(2, joint_unit(3));
z_temp = joint_coords(3, joint_unit(3));
outer_node2 = [x_temp y_temp z_temp];

bone_vec1 = outer_node1 - center_node;
bone_vec2 = outer_node2 - center_node;

included_angle = Calculate_included_angle(bone_vec1, bone_vec2);
norm_vec = Calculate_norm_vec(bone_vec1, bone_vec2);

end

