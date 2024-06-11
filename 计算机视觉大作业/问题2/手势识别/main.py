import cv2
import os
import picture as pic  # 确保这个模块存在，且binaryMask函数可用

# 设置文件夹路径
input_folder_path = '3'  # 替换为您的输入图片文件夹路径
output_folder_path = '3_out'  # 替换为您的输出图片文件夹路径

# 确保输出文件夹存在
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# # 设置手势框的参数
# x0, y0 = 300, 100  # 设置选取位置
# width, height = 251, 251  # 设置窗口大小

# 图像大小
image_width, image_height = 251, 251

# 手势框大小
gesture_box_width, gesture_box_height = 150, 150

# 设置手势框的起始位置，留出足够的边缘空间
offset = 50  # 从图像边缘向内的偏移量

# 计算手势框的起始位置
x0 = offset
y0 = offset

# 确保手势框不会超出图像边界
x0 = max(x0, 0)
y0 = max(y0, 0)
x1 = min(x0 + gesture_box_width, image_width)
y1 = min(y0 + gesture_box_height, image_height)

# 如果需要，调整手势框大小以确保它不超出图像边界
gesture_box_width = x1 - x0
gesture_box_height = y1 - y0


# 获取文件夹中所有文件的列表
files = os.listdir(input_folder_path)

# 遍历文件夹中的每个文件
for file in files:
    # 构建完整的文件路径
    file_path = os.path.join(input_folder_path, file)
    
    # 确保只处理文件夹中的图像文件
    if os.path.isfile(file_path) and file.lower().endswith(('bmp')):
        # 加载图片
        frame = cv2.imread(file_path)
        
        # 检查图片是否成功加载
        if frame is None:
            print(f"Error: Unable to load image at path {file_path}")
            continue
        
        # 应用您的处理函数
        roi = pic.binaryMask(frame, x0, y0, gesture_box_width, gesture_box_height)
        
        # 构建输出文件路径
        output_file_path = os.path.join(output_folder_path, file)
        
        # 保存处理后的图像
        cv2.imwrite(output_file_path, roi)
        
        # 如果需要，也可以在屏幕上显示图像
        cv2.imshow('ROI', roi)
        cv2.waitKey(0)

# 如果显示了图像，确保在循环结束后关闭所有窗口
cv2.destroyAllWindows()
