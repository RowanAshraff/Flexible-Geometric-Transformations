# User guide:
#   the "Horizontal" trackbar moves the video along the x-axis
#   the "Vertical" trackbar moves the video along the y-axis
#   the "Rotation" trackbar rotates the video around the center
#   Esc exits the program


import cv2
import numpy as np
refPt = []
rotation = 0
x_axis = 0
y_axis = 0


def trackbar_callback(x):
    pass


def trackbar_on_image():
    cv2.namedWindow('image')
    cv2.resizeWindow('image', 400, 120)

    # create trackbars and set their values
    cv2.createTrackbar('Horizontal', 'image', 0, 200, trackbar_callback)
    cv2.createTrackbar('Vertical', 'image', 0, 200, trackbar_callback)
    cv2.createTrackbar('Rotation', 'image', 0, 200, trackbar_callback)

    cv2.setTrackbarPos('Horizontal', 'image', 100)
    cv2.setTrackbarPos('Vertical', 'image', 100)
    cv2.setTrackbarPos('Rotation', 'image', 100)


def transformation():
    global x_axis, y_axis, rotation
    # cases for each movement(+ve and -ve direction)
    if x_axis >= 100:
        x_axis = (x_axis - 100) * 6.4
    elif x_axis < 100:
        x_axis = (100 - x_axis) * -6.4
    if y_axis >= 100:
        y_axis = (y_axis - 100) * -4.8
    elif y_axis < 100:
        y_axis = (100 - y_axis) * 4.8
    if rotation >= 100:
        rotation = (rotation - 100) * 1.8
    elif rotation < 100:
        rotation = (100 - rotation) * -1.8


# x-axis and y-axis movement
def translation(frame):
    global x_axis, y_axis
    rows, cols = frame.shape[0], frame.shape[1]
    x_axis = cv2.getTrackbarPos('Horizontal', 'image')
    y_axis = cv2.getTrackbarPos('Vertical', 'image')
    transformation()
    n = np.float32([[1, 0, x_axis], [0, 1, y_axis]])
    dst = cv2.warpAffine(frame, n, (cols, rows))
    return dst


# rotation
def rotate(frame):
    global rotation
    rows, cols = frame.shape[0], frame.shape[1]
    # matrix of transformation
    rotation = cv2.getTrackbarPos('Rotation', 'image')
    transformation()
    m = cv2.getRotationMatrix2D((cols/2, rows/2), rotation, 1)
    ## 3rd argument :(width, height) Remember width = number of columns, and height = number of rows.
    dst = cv2.warpAffine(frame, m, (cols, rows))
    return dst


def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Put the clicks coordinates in a variable
        refPt.append([x, y])
        if len(refPt) > 1:
            refPt.clear()
            refPt.append([x, y])


if __name__ == "__main__":
    trackbar_on_image()
    cap = cv2.VideoCapture(0)
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = translation(frame)
            frame = rotate(frame)
            cv2.imshow('frame', frame)
            k = cv2.waitKey(1)
            if k == 27:
                break
            elif k == ord('r'):
                cv2.setTrackbarPos('Horizontal', 'image', 100)
                cv2.setTrackbarPos('Vertical', 'image', 100)
                cv2.setTrackbarPos('Rotation', 'image', 100)
    cv2.destroyAllWindows()