import numpy as np
from PIL import Image

# 変数置き場
filter_size = 10    # ぼかしの大きさ(偶数にすること)
center_wid_pump = 332    # 取り出す画像の中心
center_hei_pump = 225    # 取り出す画像の中心
center_wid_SH = 332    # 取り出す画像の中心
center_hei_SH = 227    # 取り出す画像の中心
wid = 300   # 画像の幅(pixel)(偶数にすること)
hei = 300   # 画像の高さ(pixel)(偶数にすること)
ellipse_wid = 40.1E-3    # 楕円の幅直径(mm)
ellipse_hei = 25.2E-3    # 楕円の高さ直径(mm)
dx = 0.3157E-3   # 1pixelの大きさ(mm/pixel)
dy = 0.2969E-3   # 1pixelの大きさ(mm/pixel)
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
# ぼかし後の入れ物
amplitude_blur_pump = np.array([[0.0 for a in range(width_original - filter_size)] for a in range(height_original - filter_size)])
amplitude_blur_SH = np.array([[0.0 for a in range(width_original - filter_size)] for a in range(height_original - filter_size)])
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
        amplitude_blur_pump[h][w] = mean_partial_pump
        amplitude_blur_SH[h][w] = mean_partial_SH
        img_blur_pump.putpixel((w, h), int(mean_partial_pump))
        img_blur_SH.putpixel((w, h), int(mean_partial_SH))
# 画像(電界振幅)をarrayに変換
#amplitude_blur_pump = np.array([[img_blur_pump.getpixel((x,y)) for x in range(width_original - filter_size)] for y in range(height_original - filter_size)])
#amplitude_blur_SH = np.array([[img_blur_SH.getpixel((x,y)) for x in range(width_original - filter_size)] for y in range(height_original - filter_size)])
# モードのところだけ取り出す
amplitude_mode_pump = amplitude_blur_pump[int(center_hei_pump - hei/2):int(center_hei_pump + hei/2), int(center_wid_pump - wid/2):int(center_wid_pump + wid/2)]
amplitude_mode_SH = amplitude_blur_SH[int(center_hei_SH - hei/2):int(center_hei_SH + hei/2), int(center_wid_SH - wid/2):int(center_wid_SH + wid/2)]
# モードの部分の画像の入れ物
img_mode_pump = Image.new('L', (wid, hei))
img_mode_SH = Image.new('L', (wid, hei))
# 規格化されていない電界にする
for h in range(hei):
    for w in range(wid):
        field_mode_pump[h][w] = np.sqrt(amplitude_mode_pump[h][w])
        field_mode_SH[h][w] = np.sqrt(amplitude_mode_SH[h][w])
# 楕円の各ピクセルの値を一列に並べる(引数-1とすると自動で決定してくれる)
array_mode_pump = amplitude_mode_pump.reshape(1, -1)
array_mode_SH = amplitude_mode_SH.reshape(1, -1)
# 合計する(axis=0:列ごとの合計, axis=1:行ごとの合計)
sum_mode_pump = np.sum(array_mode_pump, axis=1)
sum_mode_SH = np.sum(array_mode_SH, axis=1)
# 規格化電界の計算
norm_mode_pump = np.sqrt(2 / (c * eps * n_pump * sum_mode_pump * dx * dy)) * field_mode_pump
norm_mode_SH = np.sqrt(2 / (c * eps * n_SH * sum_mode_SH * dx * dy)) * field_mode_SH

# κの計算
for h in range(hei):
    for w in range(wid):
        test_mode_pump += (c * eps * n_pump / 2) * norm_mode_pump[h][w]**2 * dx * dy  # 規格化の確認
        test_mode_SH += (c * eps * n_SH / 2) * norm_mode_SH[h][w]**2 * dx * dy        # 規格化の確認
        kappa_mode += (omega * eps / 2) * d33 * norm_mode_SH[h][w] * norm_mode_pump[h][w]**2 * dx * dy
        img_mode_pump.putpixel((w, h), int(amplitude_mode_pump[h][w]))
        img_mode_SH.putpixel((w, h), int(amplitude_mode_SH[h][w]))
kappa = eps * np.sqrt(2 * omega**2 / (n_pump**2 * n_SH) * (mu / eps)**(3/2) * d33**2 / (np.pi * ellipse_wid/2 * ellipse_hei/2))

print("test_mode_pump: {}".format(test_mode_pump))
print("test_mode_SH: {}".format(test_mode_SH))
print("kappa = {} W^(-1/2)mm^(-1)".format(kappa))
print("kappa_mode = {} W^(-1/2)mm^(-1)".format(kappa_mode))
print("normalized conversion efficiency = {} %/W".format(kappa**2 * L**2 * 100))
print("normalized conversion efficiency mode= {} %/W".format(kappa_mode**2 * L**2 * 100))


img_mode_pump.save('3img_mode_pump.bmp')
img_mode_SH.save('3img_mode_SH.bmp')
