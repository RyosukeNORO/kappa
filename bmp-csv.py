import numpy as np
from PIL import Image

# 変数置き場
filter_size = 10    # ぼかしの大きさ(偶数にすること)
center_wid_pump = 250    # 取り出す画像の中心
center_hei_pump = 250    # 取り出す画像の中心
center_wid_SH = 250    # 取り出す画像の中心
center_hei_SH = 250    # 取り出す画像の中心
wid = 400   # 画像の幅(pixel)(偶数にすること)
hei = 400   # 画像の高さ(pixel)(偶数にすること)
ellipse_wid = 43E-3    # 楕円の幅直径(mm)
ellipse_hei = 28E-3    # 楕円の高さ直径(mm)
dx = 0.2E-3   # 1pixelの大きさ(mm/pixel)
dy = 0.2E-3   # 1pixelの大きさ(mm/pixel)
L = 15  # デバイス長(mm)

# 定数置き場
c = 2.99792458E11    # 光速(mm/s)
eps = 8.8541878128E-15  # 真空の誘電率(F/mm)
mu = 1 / (c **2 * eps)   # 真空の透磁率(H/mm)
n_pump = 2.13   # 励起光の屈折率
n_SH = 2.20 # SH光の屈折率
d33 = 13.8E-9 * (2 / np.pi)  # 非線形光学定数(mm/V)
lam = 1030E-6  # 励起光波長(mm)
omega = 2 * np.pi * c / lam    # 励起光角周波数(rad/s)

# 入れ物の定義
amplitude_mode_pump = np.array([[0.0 for a in range(wid)] for a in range(hei)])
amplitude_mode_SH = np.array([[0.0 for a in range(wid)] for a in range(hei)])
field_mode_pump = np.array([[0.0 for a in range(wid)] for a in range(hei)])
field_mode_SH = np.array([[0.0 for a in range(wid)] for a in range(hei)])
field_mode_pump = np.array([[0.0 for a in range(wid)] for a in range(hei)])
field_mode_SH = np.array([[0.0 for a in range(wid)] for a in range(hei)])
img_mode_pump = Image.new('L', (wid, hei))
img_mode_SH = Image.new('L', (wid, hei))
test_mode_pump = 0
test_mode_SH = 0
kappa_mode = 0

# 元となる画像の読み込み
img_original_pump = Image.open('46pump.bmp')
img_original_SH = Image.open('46SH.bmp')
# オリジナル画像の幅と高さを取得
width_original, height_original = img_original_pump.size
# ぼかし後の画像の入れ物
img_blur_pump = Image.new('L', (width_original - filter_size, height_original - filter_size))
img_blur_SH = Image.new('L', (width_original - filter_size, height_original - filter_size))
# 画像(電界振幅)をarrayに変換
amplitude_original_pump = np.array([[img_original_pump.getpixel((x,y)) for x in range(width_original)] for y in range(height_original)])
amplitude_original_SH = np.array([[img_original_SH.getpixel((x,y)) for x in range(width_original)] for y in range(height_original)])
# ぼかし加工
for h in range(height_original - filter_size):
    for w in range(width_original - filter_size):
        # 位置(x,y)を起点に縦横フィルターサイズの小さい画像をオリジナル画像から切り取る
        amplitude_partial_pump = amplitude_original_pump[h:h + filter_size, w:w + filter_size]
        amplitude_partial_SH = amplitude_original_SH[h:h + filter_size, w:w + filter_size]
        # 小さい画像の各ピクセルの値を一行に並べる
        array_partial_pump = amplitude_partial_pump.reshape(1, -1)
        array_partial_SH = amplitude_partial_SH.reshape(1, -1)
        # 平均を求めて加工後画像の位置(x,y)のピクセルの値にセットする
        mean_partial_pump = array_partial_pump.mean(axis = 1)
        mean_partial_SH = array_partial_SH.mean(axis = 1)
        img_blur_pump.putpixel((w, h), int(mean_partial_pump))
        img_blur_SH.putpixel((w, h), int(mean_partial_SH))
# 画像(電界振幅)をarrayに変換
amplitude_blur_pump = np.array([[img_blur_pump.getpixel((x,y)) for x in range(width_original - filter_size)] for y in range(height_original - filter_size)])
amplitude_blur_SH = np.array([[img_blur_SH.getpixel((x,y)) for x in range(width_original - filter_size)] for y in range(height_original - filter_size)])
'''
np.savetxt('amplitude_blur_46pump.csv', amplitude_blur_pump, delimiter=',')
np.savetxt('amplitude_blur_46SH.csv', amplitude_blur_SH, delimiter=',')
'''
img_blur_pump.save('blur_46pump.bmp')
img_blur_SH.save('blur_46SH.bmp')

