import cv2
import numpy as np

def draw_contours(img, cnts):  # conts = contours
    img = np.copy(img)
    img = cv2.drawContours(img, cnts, -1, (0, 255, 0), 2)
    return img


def draw_min_rect_circle(img, cnts):  # conts = contours
    img = np.copy(img)
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # blue

        min_rect = cv2.minAreaRect(cnt)  # min_area_rectangle
        min_rect = np.int0(cv2.boxPoints(min_rect))
        cv2.drawContours(img, [min_rect], 0, (0, 255, 0), 2)  # green

        '''(x, y), radius = cv2.minEnclosingCircle(cnt)
        center, radius = (int(x), int(y)), int(radius)  # center and radius of minimum enclosing circle
        img = cv2.circle(img, center, radius, (0, 0, 255), 2)  # red'''
    return img


def draw_approx_hull_polygon(img, cnts):
    #img = np.copy(img)
    img = np.zeros(img.shape, dtype=np.uint8)

    cv2.drawContours(img, cnts, -1, (255, 0, 0), 2)  # blue

    epsilion = img.shape[0]/32
    approxes = [cv2.approxPolyDP(cnt, epsilion, True) for cnt in cnts]
    cv2.polylines(img, approxes, True, (0, 255, 0), 2)  # green

    hulls = [cv2.convexHull(cnt) for cnt in cnts]
    cv2.polylines(img, hulls, True, (0, 0, 255), 2)  # red

    return img


def run():
    image = cv2.imread('H:\Codes\IntelligentBuildingPerformanceDesign\\resources\detect.jpg')  # a black objects on white image is better
    thresh = cv2.Canny(image, 128, 256)
    thresh, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    '''for i in contours:
        averageX,averageY=0,0
        print(i.shape)
        for j in i:
            averageX+=j[0][0]
            averageY+=j[0][1]
        averageX=averageX
        averageY=averageY'''

    imgs = [image, thresh,draw_min_rect_circle(image, contours)]
    for img in imgs:
        cv2.imwrite("%s.jpg" % id(img), img)
        cv2.imshow("contours", img)


if __name__ == '__main__':
    run()
pass