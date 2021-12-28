import cv2

def HSV_method(roi):
    # reduce noise
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # hsv = cv2.GaussianBlur(hsv, (15, 15), 0)
    _, bw = cv2.threshold(hsv[:, :, 2], 0, 255,
                          cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    morph = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
    dist = cv2.distanceTransform(morph, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)

    borderSize = 40
    distborder = cv2.copyMakeBorder(dist, borderSize, borderSize, borderSize, borderSize,
                                    cv2.BORDER_CONSTANT | cv2.BORDER_ISOLATED, 0)
    gap = 10
    kernel2 = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (2*(borderSize-gap)+1, 2*(borderSize-gap)+1))
    kernel2 = cv2.copyMakeBorder(kernel2, gap, gap, gap, gap,
                                 cv2.BORDER_CONSTANT | cv2.BORDER_ISOLATED, 0)
    distTempl = cv2.distanceTransform(
        kernel2, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
    nxcor = cv2.matchTemplate(distborder, distTempl, cv2.TM_CCOEFF_NORMED)
    _, mx, _, _ = cv2.minMaxLoc(nxcor)
    _, peaks = cv2.threshold(nxcor, mx*0.45, 255, cv2.THRESH_BINARY)
    peaks8u = cv2.convertScaleAbs(peaks)
    # cv2.imshow('test', peaks)
    contours, _ = cv2.findContours(
        peaks8u, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('processing', peaks8u)
    return contours





