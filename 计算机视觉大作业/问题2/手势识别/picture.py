import cv2
import numpy as np

def binaryMask(frame, x0, y0, width, height):
    # 获取手势框图
    roi = frame[y0:y0 + height, x0:x0 + width]

    #双边滤波，9为区域的直径，后面两个参数是空间高斯函数标准差和灰度值相似性高斯函数标准差
    blur = cv2.bilateralFilter(roi,9,75,75)

    res = skinMask(blur)  # 进行肤色检测
    #cv2.imshow("res", res)  # 显示肤色检测后的图像

    kernel = np.ones((3, 3), np.uint8)  # 设置卷积核
    erosion = cv2.erode(res, kernel)  # 腐蚀操作
    dilation = cv2.dilate(erosion, kernel)  # 膨胀操作
    
    binaryimg = cv2.Canny(res, 50, 200) #二值化，canny检测
    contours, _ = cv2.findContours(binaryimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)[-2:] #寻找轮廓
    
    #cv2.drawContours(frame, contours, -1, (255, 0, 255), 2)  # 在原始图像上绘制紫色轮廓线
    cv2.drawContours(frame[y0:y0 + height, x0:x0 + width], contours, -1, (255, 0, 255), 2)  # 在原始图像上绘制紫色轮廓线
    
    #cv2.imshow("Contours", frame)  # 显示带有紫色轮廓线的原始图像
    return frame

#YCrCb颜色空间的Cr分量+Otsu法阈值分割算法
def skinMask(roi):
	YCrCb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCR_CB) #转换至YCrCb空间
	(y,cr,cb) = cv2.split(YCrCb) #拆分出Y,Cr,Cb值
	cr1 = cv2.GaussianBlur(cr, (5,5), 0)
	_, skin = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #Ostu处理
	res = cv2.bitwise_and(roi,roi, mask = skin)
	return res