import cv2

class DetectTable(object):
    def __init__(self, src_img):
        self.src_img = src_img

    def run(self):
        if len(self.src_img.shape) == 2:
            gray_img = self.src_img
        elif len(self.src_img.shape) ==3:
            gray_img = cv2.cvtColor(self.src_img, cv2.COLOR_BGR2GRAY)

        thresh_img = cv2.adaptiveThreshold(~gray_img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,-2)
        h_img = thresh_img.copy()
        v_img = thresh_img.copy()
        scale = 15
        h_size = int(h_img.shape[1]/scale)

        h_structure = cv2.getStructuringElement(cv2.MORPH_RECT,(h_size,1))
        h_erode_img = cv2.erode(h_img,h_structure,1)

        h_dilate_img = cv2.dilate(h_erode_img,h_structure,1)
        v_size = int(v_img.shape[0] / scale)

        v_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, v_size))
        v_erode_img = cv2.erode(v_img, v_structure, 1)
        v_dilate_img = cv2.dilate(v_erode_img, v_structure, 1)

        mask_img = h_dilate_img+v_dilate_img
        joints_img = cv2.bitwise_and(h_dilate_img,v_dilate_img)
        cv2.imshow("joints",joints_img)
        cv2.imshow("mask",mask_img)

        return mask_img,joints_img


if __name__=='__main__':
    image = cv2.imread('p27.png')
    cv2.imshow("img",image)
    mask,joint = DetectTable(image).run()
    cv2.waitKey()
