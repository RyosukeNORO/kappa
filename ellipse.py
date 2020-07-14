import numpy as np
from PIL import Image

# 変数置き場
wid = 225   # 画像の幅(pixel)
hei = 150   # 画像の高さ(pixel)
ellipse_wid_pump = 43E-3 #np.sqrt(10) * 1E-3    # 楕円の幅直径(mm)
ellipse_hei_pump = 28E-3 #np.sqrt(10) * 1E-3    # 楕円の高さ直径(mm)
ellipse_wid_SH = 25.256E-3 #np.sqrt(10) * 1E-3    # 楕円の幅直径(mm)
ellipse_hei_SH = 17.364E-3 #np.sqrt(10) * 1E-3    # 楕円の高さ直径(mm)
dx = 0.3157E-3   # 1pixelの大きさ(mm/pixel)
dy = 0.2969E-3   # 1pixelの大きさ(mm/pixel)
L = 15  # デバイス長(mm)

# 定数置き場
c = 2.99792458E11    # 光速(mm/s)
eps = 8.8541878128E-15  # 真空の誘電率(F/mm)
mu = 1 / (c **2 * eps)   # 真空の透磁率(H/mm)
n_pump = 2.13   #2.15    # 励起光の屈折率
n_SH = 2.20     #2.27    # SH光の屈折率
d33 = 13.8E-9 * (2 / np.pi)  # 非線形光学定数(mm/V)
lam = 1030E-6  # 励起光波長(mm)
omega = 2 * np.pi * c / lam    # 励起光角周波数(rad/s)

# 入れ物の定義
amplitude_ellipse_pump = np.array([[0.0 for a in range(wid)] for a in range(hei)])
amplitude_ellipse_SH = np.array([[0.0 for a in range(wid)] for a in range(hei)])
field_ellipse_pump = np.array([[0.0 for a in range(wid)] for a in range(hei)])
field_ellipse_SH = np.array([[0.0 for a in range(wid)] for a in range(hei)])
img_ellipse_pump = Image.new('L', (wid, hei))
img_ellipse_SH = Image.new('L', (wid, hei))
test_ellipse_pump = 0
test_ellipse_SH = 0
kappa_ellipse = 0

# 楕円を作る
for h in range(hei):
    for w in range(wid):
        field_ellipse_pump[h][w] = np.exp(-(2 * (w - wid / 2) * dx / ellipse_wid_pump) ** 2) * np.exp(-(2 * (h - hei / 2) * dy / ellipse_hei_pump) ** 2)
        field_ellipse_SH[h][w] = np.exp(-(2 * (w - wid / 2) * dx / ellipse_wid_SH) ** 2) * np.exp(-(2 * (h - hei / 2) * dy / ellipse_hei_SH) ** 2)
        amplitude_ellipse_pump[h][w] = field_ellipse_pump[h][w]**2
        amplitude_ellipse_SH[h][w] = field_ellipse_SH[h][w]**2
        img_ellipse_pump.putpixel((w, h), int(round(amplitude_ellipse_pump[h][w] * 255)))
        img_ellipse_SH.putpixel((w, h), int(round(amplitude_ellipse_SH[h][w] * 255)))

# 楕円の各ピクセルの値を一列に並べる(引数-1とすると自動で決定してくれる)
array_ellipse_pump = amplitude_ellipse_pump.reshape(1, -1)
array_ellipse_SH = amplitude_ellipse_SH.reshape(1, -1)
# 合計する(axis=0:列ごとの合計, axis=1:行ごとの合計)
sum_ellipse_pump = np.sum(array_ellipse_pump, axis=1)
sum_ellipse_SH = np.sum(array_ellipse_SH, axis=1)
# 規格化電界の計算
norm_ellipse_pump = np.sqrt(2 / (c * eps * n_pump * sum_ellipse_pump * dx * dy)) * field_ellipse_pump
norm_ellipse_SH = np.sqrt(2 / (c * eps * n_SH * sum_ellipse_SH * dx * dy)) * field_ellipse_SH

# κの計算
for h in range(hei):
    for w in range(wid):
        test_ellipse_pump += (c * eps * n_pump / 2) * norm_ellipse_pump[h][w]**2 * dx * dy  # 規格化の確認
        test_ellipse_SH += (c * eps * n_SH / 2) * norm_ellipse_SH[h][w]**2 * dx * dy        # 規格化の確認
        kappa_ellipse += (omega * eps / 2) * d33 * norm_ellipse_SH[h][w] * norm_ellipse_pump[h][w]**2 * dx * dy
kappa = eps * np.sqrt(2 * omega**2 / (n_pump**2 * n_SH) * (mu / eps)**(3/2) * d33**2 / (np.pi * ellipse_wid_pump/2 * ellipse_hei_pump/2))

print("test_ellipse_pump: {}".format(test_ellipse_pump))
print("test_ellipse_SH: {}".format(test_ellipse_SH))
print("kappa = {} W^(-1/2)mm^(-1)".format(kappa))
print("kappa_ellipse = {} W^(-1/2)mm^(-1)".format(kappa_ellipse))
'''
img_ellipse_pump.show()
img_ellipse_SH.show()
'''
img_ellipse_pump.save("ellipse_pump.bmp")
img_ellipse_SH.save("ellipse_SH.bmp")
