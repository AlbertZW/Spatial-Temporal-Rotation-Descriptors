import numpy as np
import math

class rotationAnglesRep:
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

	def _included_angle(self, vec1, vec2):
		if ((vec1 == vec2).all()):
			included_ang = 0
		else:
			dotProd = np.dot(vec1, vec2)
			normProd = math.sqrt(np.dot(vec1, vec1) * np.dot(vec2, vec2))
			if normProd == 0:
				included_ang = 0
			else:
				cosined_angle = dotProd / normProd
				if cosined_angle > 1:
					cosined_angle = 1
				elif cosined_angle < -1:
					cosined_angle = -1
				included_ang = np.arccos(cosined_angle)
		return included_ang

	def _cross_prod(self, vec1, vec2):
		# b1c2-b2c1,c1a2-a1c2,a1b2-a2b1
		x = vec1[1] * vec2[2] - vec2[1] * vec1[2]
		y = vec1[2] * vec2[0] - vec2[2] * vec1[0]
		z = vec1[0] * vec2[1] - vec2[0] * vec1[1]
		return np.array([x, y, z])

	def _norm_vec(self, vec1, vec2):
		if ((vec1 == vec2).all()):
			return np.array([1, 0, 0])
		else:
			unnormed_vec = self._cross_prod(vec1, vec2)
			norm = np.sqrt(unnormed_vec.dot(unnormed_vec))
			if norm == 0:
				return np.array([1, 0, 0])
			else:
				return unnormed_vec / norm

	def _Rodriguez(self, vec1, vec2):
		rotationMatrix = np.zeros((3, 3))

		if (vec1 == np.array([0, 0, 0])).all() or (vec2 == np.array([0, 0, 0])).all() or (vec1 == vec2).all():
			rotationMatrix[0, 0] = 1
			rotationMatrix[1, 1] = 1
			rotationMatrix[2, 2] = 1

		else:
			norm_vec1 = np.sqrt(vec1.dot(vec1))
			vec1 = vec1 / norm_vec1
			norm_vec2 = np.sqrt(vec2.dot(vec2))
			vec2 = vec2 / norm_vec2

			rotationAxis = self._norm_vec(vec1, vec2)
			rotationAngle = self._included_angle(vec1, vec2)

			rotationMatrix[0, 0] = math.cos(rotationAngle) + rotationAxis[0] * rotationAxis[0] * (1 - math.cos(rotationAngle))
			rotationMatrix[0, 1] = rotationAxis[0] * rotationAxis[1] * (1 - math.cos(rotationAngle)) - rotationAxis[2] * math.sin(rotationAngle)
			rotationMatrix[0, 2] = rotationAxis[1] * math.sin(rotationAngle) + rotationAxis[0] * rotationAxis[2] * (1 - math.cos(rotationAngle))

			rotationMatrix[1, 0] = rotationAxis[2] * math.sin(rotationAngle) + rotationAxis[0] * rotationAxis[1] * (1 - math.cos(rotationAngle))
			rotationMatrix[1, 1] = math.cos(rotationAngle) + rotationAxis[1] * rotationAxis[1] * (1 - math.cos(rotationAngle))
			rotationMatrix[1, 2] = -rotationAxis[0] * math.sin(rotationAngle) + rotationAxis[1] * rotationAxis[2] * (1 - math.cos(rotationAngle))

			rotationMatrix[2, 0] = -rotationAxis[1] * math.sin(rotationAngle) + rotationAxis[0] * rotationAxis[2] * (1 - math.cos(rotationAngle))
			rotationMatrix[2, 1] = rotationAxis[0] * math.sin(rotationAngle) + rotationAxis[1] * rotationAxis[2] * (1 - math.cos(rotationAngle))
			rotationMatrix[2, 2] = math.cos(rotationAngle) + rotationAxis[2] * rotationAxis[2] * (1 - math.cos(rotationAngle))

		return rotationMatrix


	def _rotateVec1ToX(self, vec1, vec2):
		rotation = self._Rodriguez(vec1, np.array([1, 0, 0]))
		normalized_vec2 = np.matmul(rotation, vec2.transpose())

		return normalized_vec2


	def _normalize_joint(self, original_node, joint_unit):
		normalized_vec2_list = []
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

			normalized_vec2 = self._rotateVec1ToX(bone_vec1, bone_vec2)

			normalized_vec2_list.append(normalized_vec2)
		return normalized_vec2_list

	def _calculate_JointRotationFeature(self, data_prev, data_curr, joint_structure):
		skeleton_num = data_prev.shape[2]
		joint_rotation_feature = np.zeros((3, len(joint_structure), skeleton_num))
		for i in range(29):
			joint_unit = joint_structure[i]

			normalized_vec2_prev = self._normalize_joint(data_prev, joint_unit)
			normalized_vec2_curr = self._normalize_joint(data_curr, joint_unit)
			
			for m in range(skeleton_num):
				vec2_prev = normalized_vec2_prev[m]
				vec2_curr = normalized_vec2_curr[m]

				rotation_axis = self._norm_vec(vec2_prev, vec2_curr)
				psi = self._included_angle(vec2_prev, vec2_curr)

				phi = self._included_angle(np.array([1, 0, 0]), rotation_axis)
				theta = self._included_angle(np.array([0, 0, 1]), rotation_axis)
				
				joint_rotation_feature[0, i, m] = phi
				joint_rotation_feature[1, i, m] = theta
				joint_rotation_feature[2, i, m] = psi
		
		return joint_rotation_feature

	def getJointRotationFeature(self, frames_data):
		frame_num = frames_data.shape[1]
		skeleton_num = frames_data.shape[3]
		joint_rotation_feature = np.zeros((3, frame_num - 1, len(self.joints), skeleton_num))

		for frame_index in range(1, frame_num):
			data_prev = frames_data[:, frame_index - 1, :, :]
			data_curr = frames_data[:, frame_index, :, :]

			rotation_feature = self._calculate_JointRotationFeature(data_prev, data_curr, self.joints)
			joint_rotation_feature[:, frame_index - 1, :, :] = rotation_feature

		return joint_rotation_feature


# test1 = np.array([1, 1, 0])
# test2 = np.array([0, 1, 1])
# print(norm_vec(test1, test2))