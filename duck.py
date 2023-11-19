import cv2
import numpy as np

# 读取图片
image = cv2.imread(r'C:\Users\Administrator\Desktop\rice\e52683b51e5d7b060b96fb53fab14c5.png')
# 确保图像不为空
if image is None:
    ...
else:
    # 将图片从BGR转换到HSV颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义黄色的HSV范围
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # 根据黄色范围创建掩码
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # 寻找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 绘制轮廓
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # 可以根据面积大小过滤噪点
        if area > 300:
            x, y, w, h = cv2.boundingRect(cnt)
            # 在原图上画出矩形框
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            print(x+w/2, y+h/2)
    # 显示带有矩形框的原图像
    cv2.imshow('Image with Bounding Boxes', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()