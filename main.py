import sys

import cv2
import numpy as np

# 評価項目数
ITEM_N = 6
# ユーザーごとの評価値
USER_VALUE_LIST = [
    [7, 2, 3, 4, 1, 2],
    [5, 7, 1, 3, 3, 5],
    [2, 4, 7, 3, 4, 5],
    [3, 5, 2, 7, 2, 3],
    [2, 3, 5, 2, 7, 1],
    [1, 1, 2, 5, 5, 7]
]

# 画像サイズ
CAMVAS_SIZE = 1800

# 円弧の描画数
CIRCLE_NUM = 5
# 円の中心座標
CENTER_C = int(CAMVAS_SIZE / 2)

# 軸の長さ（中心からの）
LINE_L = 750


# いい感じにグラデーションのRGB値を返す
def colorBar(x):
    sts = [0.25, 0.5, 0.75]

    if x < sts[0]:
        R = 0.0
        B = 1.0
        G = np.sin(x * 4 * np.pi * 0.5)
    elif x < sts[1]:
        R = 0.0
        G = 1.0
        B = np.sin((x - sts[0]) * 4 * np.pi * 0.5 + (np.pi * 0.5))
    elif x < sts[2]:
        R = np.sin((x - sts[1]) * 4 * np.pi * 0.5)
        G = 1.0
        B = 0.0
    else:
        R = 1.0
        G = np.sin((x - sts[2]) * 4 * np.pi * 0.5 + (np.pi * 0.5))
        B = 0.0

    return (R * 255, G * 255, B * 255)


# 角度と長さより点の座標を計算
def calc_point(theta, length):
    x_coord = CENTER_C + np.cos(-theta + (np.pi / 2)) * length
    y_coord = CENTER_C - np.sin(-theta + (np.pi / 2)) * length
    return int(x_coord), int(y_coord)


def main():
    if ITEM_N != len(USER_VALUE_LIST[1]):
        print("項目数と与えられたデータのサイズが一致してないっぽい")
        sys.exit()

    # キャンバス用意
    img = np.full((CAMVAS_SIZE, CAMVAS_SIZE, 3), 255, dtype=np.uint8)

    # 円弧の描画
    for c_size in range(1, CIRCLE_NUM + 1):
        cv2.circle(img, (CENTER_C, CENTER_C), c_size * 100, (50, 50, 50), thickness=2, lineType=cv2.LINE_AA)

    # 軸の描画
    for theta in range(ITEM_N):
        x, y = calc_point((theta / ITEM_N) * 2 * np.pi, LINE_L)
        cv2.line(img, (x, y), (CENTER_C, CENTER_C), (50, 50, 50), thickness=3, lineType=cv2.LINE_AA)

    # 各ユーザの描画
    for u_i, user in enumerate(USER_VALUE_LIST):
        pts = []
        for nth, point in enumerate(user):
            x, y = calc_point((nth / ITEM_N) * 2 * np.pi, point * 100)
            pts.append([int(x), int(y)])

        pts = np.array(pts, np.int32)
        pts = pts.reshape((-1, 1, 2))
        # print("color", float(u_i / (len(USER_VALUE_LIST) - 1)))
        color_t = colorBar(1 - float(u_i / (len(USER_VALUE_LIST) - 1)))
        # print(color_t, len(USER_VALUE_LIST), u_i)
        cv2.polylines(img, [pts], True, color_t, thickness=15)

    # 画像の保存
    cv2.imwrite('opencv_draw_test.png', img)


if __name__ == '__main__':
    main()
