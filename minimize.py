import numpy as np
import cv2
from scipy.optimize import minimize
def rigid_transform(params, p):
    rotation = params[:9].reshape(3, 3)
    translation = params[9:]
    transformed = np.dot(p, rotation.T) + translation
    return transformed

# 定义损失函数
def loss_function(params, p1, p2):
    transformed_points = rigid_transform(params, p1)
    diff = transformed_points - p2
    error = np.sum(np.square(diff))
    return error

# 你的点集
scale = 1.1707786
original = cv2.imread('chessboard1.png',)
ret, corners = cv2.findChessboardCorners(original, (10, 6), None)

point_set1 = np.hstack([(corners * scale).reshape(-1, 2), np.full((corners.shape[0], 1), 288)])
point_set1[:, [0, 1]] = point_set1[:, [1, 0]]
point_set2 = np.array([[0,600,288],[0,625,288],[0,650,288],[0,675,288],[0,700,288],[0,725,288],[0,750,288],[0,775,288],[0,800,288],[0,825,288],
                          [25,600,288],[25,625,288],[25,650,288],[25,675,288],[25,700,288],[25,725,288],[25,750,288],[25,775,288],[25,800,288],[25,825,288],
                            [50,600,288],[50,625,288],[50,650,288],[50,675,288],[50,700,288],[50,725,288],[50,750,288],[50,775,288],[50,800,288],[50,825,288],
                            [75,600,288],[75,625,288],[75,650,288],[75,675,288],[75,700,288],[75,725,288],[75,750,288],[75,775,288],[75,800,288],[75,825,288],
                            [100,600,288],[100,625,288],[100,650,288],[100,675,288],[100,700,288],[100,725,288],[100,750,288],[100,775,288],[100,800,288],[100,825,288],
                            [125,600,288],[125,625,288],[125,650,288],[125,675,288],[125,700,288],[125,725,288],[125,750,288],[125,775,288],[125,800,288],[125,825,288]
                       ])
num_points = 60
original_points = point_set1
original_points=original_points[:num_points]
target_points = point_set2
target_points=target_points[:num_points]

# 初始参数矩阵，这里使用单位矩阵和零向量作为初始猜测
initial_params = np.concatenate([np.eye(3).flatten(), np.zeros(3)])

# 使用最小化函数找到最优参数
result = minimize(loss_function, initial_params, args=(original_points, target_points))

# 从优化结果中提取旋转矩阵和平移向量
optimal_rotation = result.x[:9].reshape(3, 3)
optimal_translation = result.x[9:]

print("优化后的旋转矩阵：")
print(optimal_rotation)
print("优化后的平移向量：")
print(optimal_translation)

point=np.array([  193,541,  288/scale])*scale 
print(point)
point_after_transform = np.dot(point, optimal_rotation.T) + optimal_translation
print(point_after_transform)