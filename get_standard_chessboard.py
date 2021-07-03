import cv2
import numpy as np


def get_standard_chessboard(
        x, y, interval=10, diameter=0, direction_circle=False):
    x, y = y, x  # 懶得改了，偷懶一下
    x += 1
    y += 1
    img = np.full([x * interval, y * interval, 3], 0, np.uint8)
    tmp = True
    for i in range(x):
        # tmp = not tmp
        for j in range(y):
            color = [255, 255, 255] if tmp else [0, 0, 0]
            cv2.rectangle(img,
                          (j * interval,
                           i * interval),
                          (j * interval + interval,
                           i * interval + interval),
                          color, -1)
            tmp = not tmp
        if not y % 2:
            tmp = not tmp
    if direction_circle:
        x, y = y, x  # 懶得改了，偷懶一下
        img = draw_direction_circle(img, x, y, interval, diameter)
    return img


def draw_direction_circle(img, x, y, interval=10, diameter=0):
    w, h, d = img.shape
    i = interval
    hi = int(i / 2)
    if diameter == 0:
        diameter = int(i / 4)
    if diameter <= 0:
        raise ValueError(f"diameter = {diameter}, diameter <= 0")
    if x % 2:
        if y % 2:
            # print('2-1')
            new_x = int(x * i / 2)
            new_y = int(y * i / 2)
        else:
            # print('2-2')
            new_x = int(x * i / 2)
            new_y = int(y * i / 2) + hi

    else:
        if y % 2:
            # print('3-1')
            new_x = int(x * i / 2) - hi
            new_y = int(y * i / 2)
        else:
            # print('3-2')
            new_x = int(x * i / 2) - hi
            new_y = int(y * i / 2) + hi
    color_1 = (0, 0, 0)
    color_2 = (255, 255, 255)
    if img[new_x, new_y][0] == 0:
        color_1, color_2 = color_2, color_1
    cv2.circle(img, (new_x, new_y), diameter, color_1, -1)
    cv2.circle(img, (new_x + i, new_y), diameter, color_2, -1)
    cv2.circle(img, (new_x, new_y - i), diameter, color_2, -1)
    return img


def get_SB_standard_chessboard(
        x, y, interval=10, diameter=0, direction_circle=True):
    # 取得標準棋盤
    img = get_standard_chessboard(x - 2, y - 2, interval)
    # 畫中間圓圈定方向
    if direction_circle:
        img = draw_direction_circle(img, x - 1, y - 1, interval, diameter)

    # 周邊先新增白邊
    w, h, d = img.shape
    i = interval
    w2 = w + 4 * interval
    h2 = h + 4 * interval
    img2 = np.full([w2, h2, 3], 255, np.uint8)
    img2[i * 2:w2 - i * 2, i * 2:h2 - i * 2] = img
    img = img2

    # 畫四邊圓形
    color = (0, 0, 0)
    hi = int(i / 2)
    # 先畫上、下
    _x = hi + 2 * i
    _y = i * 2 - hi + i
    if img[_x, _y][0] == 0:
        jump = False
    else:
        jump = True
    for j in range(0, x - 1):
        _x = j * i + hi + 2 * i
        if y % 2:  # 有可能遇到 x 是奇數的，這樣要左右交錯
            if jump:
                # print('4-1')
                _y = i * 2 - hi
                cv2.circle(img, (_x, _y), hi, color, -1)
                cv2.rectangle(img,
                              (_x - hi, _y),
                              (_x + hi, _y + hi),
                              color, -1)
            else:
                # print('4-2')
                _y = i * (y + 2) - hi
                cv2.circle(img, (_x, _y), hi, color, -1)
                cv2.rectangle(img,
                              (_x + hi, _y - hi),
                              (_x - hi, _y),
                              color, -1)
        else:
            if jump:
                # print('5-1')
                cv2.circle(img, (_x, _y - i), hi, color, -1)
                cv2.circle(img,
                           (_x, i * (y + 2) - hi),
                           hi, color, -1)
                cv2.rectangle(img,
                              (_x - hi, _y - i),
                              (_x + hi, _y - hi),
                              color, -1)
                cv2.rectangle(img,
                              (_x - hi, i * (y + 2) - 2 * hi),
                              (_x + hi, i * (y + 2) - hi),
                              color, -1)
        jump = not jump

    # 再畫左右(但最下面 "1/4矩形+圓" 的另外處理)
    _x = 2 * i - hi
    jump = False
    for k in range(0, y - 1):
        _y = i * 2 + k * i + hi
        if x % 2:  # 有可能遇到 y 是奇數的，這樣要左右交錯
            if jump:
                # print('6-1')
                # 右圓形
                cv2.circle(img, (_x + x * i, _y), hi, color, -1)
                # 右矩形
                cv2.rectangle(img,
                              (_x + x * i - hi, _y - hi),
                              (_x + x * i, _y + hi),
                              color, -1)
            else:
                # print('6-2')
                # 左圓形
                cv2.circle(img, (_x, _y), hi, color, -1)
                # 左矩形
                cv2.rectangle(img,
                              (_x, _y - hi),
                              (_x + hi, _y + hi),
                              color, -1)
        else:  # x是偶數，左右同y
            # print('7-1')
            if not jump:
                # 左圓形
                cv2.circle(img, (_x, _y), hi, color, -1)
                # 右圓形
                cv2.circle(img, (_x + x * i, _y), hi, color, -1)
                # 左矩形
                cv2.rectangle(img,
                              (_x, _y - hi),
                              (_x + hi, _y + hi),
                              color, -1)
                # 右矩形
                cv2.rectangle(img,
                              (_x + x * i - hi, _y - hi),
                              (_x + x * i, _y + hi),
                              color, -1)
        jump = not jump
    # 處理 "1/4矩形+圓"
    if x % 2:  # 奇
        if y % 2:  # 奇 #右上左下
            # 右上圓
            cv2.circle(img, (_x + x * i, _y - i * (y - 1)),
                       hi, color, -1)
            # 右上矩形
            cv2.rectangle(img,
                          (_x + x * i - hi, _y - i * (y - 1)),
                          (_x + x * i, _y - i * (y - 1) + hi),
                          color, -1)
            # 左下圓
            cv2.circle(img, (_x, _y + i), hi, color, -1)
            # 左下矩形
            cv2.rectangle(img,
                          (_x, _y + hi),
                          (_x + hi, _y + i),
                          color, -1)
        else:  # 偶 #右上右下
            # 右上圓
            cv2.circle(img, (_x + x * i, _y - i * (y - 1)),
                       hi, color, -1)
            # 右上矩形
            cv2.rectangle(img,
                          (_x + x * i - hi, _y - i * (y - 1)),
                          (_x + x * i, _y - i * (y - 1) + hi),
                          color, -1)
            # 右下圓
            cv2.circle(img, (_x + x * i, _y + i), hi, color, -1)
            # 右下矩形
            cv2.rectangle(img,
                          (_x + x * i - hi, _y + hi),
                          (_x + x * i - hi + hi, _y + i),
                          color, -1)
    else:
        if y % 2:  # 奇 #左下右下
            # 左下圓
            cv2.circle(img, (_x, _y + i), hi, color, -1)
            # 左下矩形
            cv2.rectangle(img,
                          (_x, _y + hi),
                          (_x + hi, _y + i),
                          color, -1)
            # 右下圓
            cv2.circle(img, (_x + x * i, _y + i), hi, color, -1)
            # 右下矩形
            cv2.rectangle(img,
                          (_x + x * i - hi, _y + hi),
                          (_x + x * i - hi + hi, _y + i),
                          color, -1)

    # 最後補4個角落，提示留白區域
    h, w, d = img.shape
    hhi = int(i / 4)
    # 左上
    cv2.rectangle(img,  (0, 0),  (hhi, hhi), color, -1)
    # 右上
    cv2.rectangle(img,  (w - hhi, 0),  (w, hhi), color, -1)
    # # 右下
    cv2.rectangle(img,  (w - hhi, h - hhi),  (w, h), color, -1)
    # # 左下
    cv2.rectangle(img,  (0, h - hhi),  (hhi, h), color, -1)
    return img


x = 14
y = 9
interval = 30
img1 = get_standard_chessboard(x, y, interval, direction_circle=True)
img2 = get_SB_standard_chessboard(x, y, interval)
cv2.imshow('img1', img1)
cv2.imshow('img2', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite('./standard_chessboard.png', img1)
cv2.imwrite('./SB_standard_chessboard.png', img2)
#
