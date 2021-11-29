import numpy as np

class LowDOFRep:
	def __init__(self):  # C * T * V * M   [3, T, 25, 2]
		# ordering nodes for the features
		# 29 joints
		self.joints = [
			# left arm
			(24, 12, 25), (24, 12, 11), (25, 12, 11), (12, 11, 10), (11, 10, 9),
			# right arm
			(22, 8, 23), (22, 8, 7), (23, 8, 7), (8, 7, 6), (7, 6, 5),
			# head and chest
			(10, 9, 21), (6, 5, 21), (9, 21, 3), (5, 21, 3), (9, 21, 5),
			(9, 21, 2), (5, 21, 2), (3, 21, 2), (4, 3, 21),
			# spinal and waist
			(21, 2, 1), (17, 1, 2), (13, 1, 2), (17, 1, 13), (18, 17, 1), (14, 13, 1),
			# left leg
			(19, 18, 17), (20, 19, 18),
			# right leg
			(15, 14, 13), (16, 15, 14)
		]

	def getFeatureLength(self):
		return len(self.joints)

	def getJointRotationFeature(self, frames_data):
		frame_num = frames_data.shape[1]
		skeleton_num = frames_data.shape[3]
		joint_rotation_feature = np.zeros((2, frame_num - 1, len(self.joints), skeleton_num))

		for frame_index in range(1, frame_num):
			data_prev = frames_data[:, frame_index - 1, :, :]
			data_curr = frames_data[:, frame_index, :, :]

			rotation_feature = self._calculate_JointRotationFeature(data_prev, data_curr, self.joints)
			joint_rotation_feature[:, frame_index - 1, :, :] = rotation_feature

		return joint_rotation_feature

	def _included_angle(self, vec1, vec2):
		dotProd = np.dot(vec1, vec2)
		normProd = np.sqrt(np.dot(vec1, vec1) * np.dot(vec2, vec2))
		cosined_angle = dotProd / normProd
		included_ang = np.arccos(cosined_angle)
		return included_ang

	def _cross_prod(self, vec1, vec2):
		# b1c2-b2c1,c1a2-a1c2,a1b2-a2b1
		x = vec1[1] * vec2[2] - vec2[1] * vec1[2]
		y = vec1[2] * vec2[0] - vec2[2] * vec1[0]
		z = vec1[0] * vec2[1] - vec2[0] * vec1[1]
		return np.array([x, y, z])

	def _norm_vec(self, vec1, vec2):
		unnormed_vec = self._cross_prod(vec1, vec2)
		norm = np.sqrt(unnormed_vec.dot(unnormed_vec))
		return unnormed_vec / norm

	def _calculate_JointRotationStatus(self, original_node, joint_unit):
		rotation_status = []
		skeleton_num = original_node.shape[2]
		for m in range(skeleton_num):
			# for outer node1
			x_temp_out = original_node[0, joint_unit[0] - 1, m]
			y_temp_out = original_node[1, joint_unit[0] - 1, m]
			z_temp_out = original_node[2, joint_unit[0] - 1, m]
			outer_node1 = np.array([x_temp_out, y_temp_out, z_temp_out])

			x_temp_out = original_node[0, joint_unit[1] - 1, m]
			y_temp_out = original_node[1, joint_unit[1] - 1, m]
			z_temp_out = original_node[2, joint_unit[1] - 1, m]
			center_node = np.array([x_temp_out, y_temp_out, z_temp_out])

			x_temp_out = original_node[0, joint_unit[2] - 1, m]
			y_temp_out = original_node[1, joint_unit[2] - 1, m]
			z_temp_out = original_node[2, joint_unit[2] - 1, m]
			outer_node2 = np.array([x_temp_out, y_temp_out, z_temp_out])

			bone_vec1 = outer_node1 - center_node
			bone_vec2 = outer_node2 - center_node

			included_angle = self._included_angle(bone_vec1, bone_vec2)
			norm_vec       = self._norm_vec(bone_vec1, bone_vec2)

			rotation_status.append((included_angle, norm_vec))
		return rotation_status

	def _calculate_JointRotationFeature(self, data_prev, data_curr, joint_structure):
		skeleton_num = data_prev.shape[2]
		joint_rotation_feature = np.zeros((2, len(joint_structure), skeleton_num))
		for i in range(len(joint_structure)):
			joint_unit = joint_structure[i]

			rotation_stat_prev = self._calculate_JointRotationStatus(data_prev, joint_unit)
			rotation_stat_curr = self._calculate_JointRotationStatus(data_curr, joint_unit)
			
			for m in range(skeleton_num):
				included_angle_prev = rotation_stat_prev[m][0]
				included_angle_curr = rotation_stat_curr[m][0]
				included_angle_diff = included_angle_curr - included_angle_prev
				
				norm_vec_prev = rotation_stat_prev[m][1]
				norm_vec_curr = rotation_stat_curr[m][1]
				norm_vec_rotation = self._included_angle(norm_vec_prev, norm_vec_curr)
				
				joint_rotation_feature[0, i, m] = included_angle_diff
				joint_rotation_feature[1, i, m] = norm_vec_rotation
		
		return joint_rotation_feature

# test1 = np.array([1, 1, 0])
# test2 = np.array([0, 1, 1])
# print(norm_vec(test1, test2))