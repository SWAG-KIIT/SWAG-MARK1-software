import cv2
import numpy as np
import matplotlib.pyplot as plt

img_org = cv2.imread('D:/t5.jpg', 0)
plt.imshow(img_org)
plt.show()
a, img = cv2.threshold(img_org, 230, 255, cv2.THRESH_BINARY+ cv2.THRESH_OTSU)
#img = cv2.adaptiveThreshold(img_org)
#img = cv2.erode(img, kernel=(4, 4), iterations=4)
img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel=(4, 4))
# edges = img
height, width = img.shape
mask = np.zeros_like(img)

polygon = np.array([[(0, height * 0.1), (width, height * 0.1), (width, height), (0, height)]], np.int32)
cv2.fillPoly(mask, polygon, 255)
masked_image = cv2.bitwise_and(img, mask)
masked_image = cv2.morphologyEx(masked_image, cv2.MORPH_OPEN, kernel=(5,5))
masked_image = cv2.dilate(masked_image, kernel=(10, 10), iterations=10)
cv2.imshow('win', masked_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
edge = 0

training_set = np.array([])
training_label = np.array([])
while (edge < img_org.shape[1]):
    temp = masked_image[edge:edge + 40]
    imgContours, contour, npaHierarchy = cv2.findContours(temp.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contour)):
        disp_img = img_org.copy()
        temp_img = img_org[edge:edge + 40].copy()
        if cv2.contourArea(contour[i]) < 1000:
            cv2.drawContours(temp_img, contour, i, (255), -1)
            rect = cv2.boundingRect(contour[i])
            x, y, w, h = rect
            cent_x = x+w//2
            data = temp_img[0:40, cent_x-20:cent_x+20]
            store = img_org[edge:edge+40, cent_x-20:cent_x+20]
            np.append(training_set, store)
            cv2.rectangle(temp_img, (cent_x - 20, 0), (cent_x + 20, 39), (255), 1)
            disp_img[edge:edge + 40] = temp_img
            cv2.imshow('win', disp_img)
            key = cv2.waitKey(0)
            cv2.destroyAllWindows()
            if key == ord('y'):
                training_set = np.append(training_label, [1, 0])
            else:
                training_label = np.append(training_label, [0, 1])
            print(w)
    edge+=40

print(len(training_set))

#np.savez('D:/Raspberry-Pi-Self-Driving-Car/computer/lane_data.npz', train=training_set, train_labels=training_label)
