import cv2
import numpy as np
import os

class ImageBarUI:
    def __init__(self, upd_func, trackbars):
        self.WINDOW_NAME = 'main_window'
        cv2.namedWindow(self.WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.WINDOW_NAME, 500, 600)

        self.upd_func = upd_func
        self.trackbars = trackbars
        self.img = None
        for (name, mn, mx, dflt) in trackbars:
            cv2.createTrackbar(name, self.WINDOW_NAME, dflt - mn, mx - mn, lambda x: None)

    def redraw_img(self):
        cv2.imshow(self.WINDOW_NAME, self.img)

    def run(self):
        k = 0
        while k != 27:
            k = cv2.waitKey(100) & 0xFF

            args = {}
            for (name, mn, mx, _) in self.trackbars:
                args[name] = cv2.getTrackbarPos(name, self.WINDOW_NAME) + mn

            if self.img is None:
                self.img = self.upd_func(**args)

            if k == ord('x'):
                self.img = self.upd_func(**args)

            self.redraw_img()

        cv2.startWindowThread()
        cv2.destroyAllWindows()


fname = os.sys.argv[1]
img = cv2.imread("%s" % fname)
gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def upd(blur=0, **kwargs):
    global gimg
    circles = cv2.HoughCircles(gimg, cv2.HOUGH_GRADIENT, **kwargs)
    timg = img.copy()
    if circles is None:
        return timg
    (_, cirCnt, _) = circles.shape
    for i in circles[0, :]:
        cv2.circle(timg, (i[0], i[1]), i[2], (0, 255, 0), 2)
        cv2.circle(timg, (i[0], i[1]), 2, (0, 0, 255), 3)
    return timg


ui = ImageBarUI(upd, [('dp', 1, 2, 1),
                      ('minDist', 1, 20, 1),
                      ('param1', 1, 100, 50),
                      ('param2', 1, 100, 30),
                      ('minRadius', 0, 100, 1),
                      ('maxRadius', 0, 100, 1)])
ui.run()
