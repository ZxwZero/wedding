# coding=utf-8
# python3

"""
Name: qr_code_gen.py
Author: xiangwei.zheng
Time: 2021-03-19 16:38
Desc: 生成二维码
"""

import qrcode
from PIL import Image


def mk_qr(url, icon_path, save_path):
    qr = qrcode.QRCode(
        version=5,  # 黑码密集程度
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 高容错率
        box_size=10,  # 二维码大小
        border=2,  # 边距
    )
    factor = 3.7  # 调整内部icon

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image()
    img = img.convert("RGBA")
    icon = Image.open(icon_path)
    img_w, img_h = img.size

    size_w = int(img_w / factor)
    size_h = int(img_h / factor)

    # icon尺寸不得超过二维码尺寸
    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)  # 重置icon大小
    icon = icon.convert("RGBA")

    w = int((img_w - icon_w)/2)  # 确定位置
    h = int((img_h - icon_h)/2)
    img.paste(icon, (w, h), icon)  # 添加中间的图标

    img.save(save_path, quality=100)   # 保存


if __name__ == '__main__':
    # sale_url = "http://10.220.32.154:9000"  # 本地
    sale_url = "http://1.117.213.193"  # 线上
    icon_img = './files/wedding_logo.jpg'  # 中间图标
    qr_code_img = "./files/wedding.png"  # 生成的二维码图片
    mk_qr(sale_url, icon_img, qr_code_img)



