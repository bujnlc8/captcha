# coding=utf-8

import os
import random

from PIL import Image, ImageDraw, ImageFont

try:
    from cStringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO


defaultFont = ImageFont.truetype(os.path.join(os.path.dirname(__file__), "fonts", "IndieFlower-Regular.ttf"), size=30)


class ImageCaptcha(object):
    def __init__(self, width=200, height=100, font=None, background=(255, 245, 238)):
        self.width = width
        self.height = height
        self.font = font if font else defaultFont
        self.draw = None
        self.data = None
        self.text = None
        self.background = background

    def _draw_text(self):
        text = self.text
        if not text:
            raise ValueError("Please specify the text to draw")
        self.draw = ImageDraw.Draw(self.im)
        # 画16根随机线条
        for x in range(16):
            # 随机生成画线的点
            first_dot = (random.randint(-10, int(self.width / 2)),
                         random.randint(-10, self.height))
            second_dot = (random.randint(int(self.width / 2),
                                         self.width + 10), random.randint(0, self.height + 10))
            # 随机生成颜色
            color = tuple({random.randint(0, 255) for x in range(4)})
            # 线条粗细
            thickness = int(random.random() * 3)
            self.draw.line(first_dot + second_dot, fill=color,
                           width=thickness, joint="curve")
        # 画一些随机颜色的点
        for x in range(random.randint(120, 150)):
            point = (random.randint(0, self.width),
                     random.randint(0, self.height))
            # 随机生成颜色
            color = tuple({random.randint(0, 255) for x in range(4)})
            self.draw.point(point, color)

        # 画文字
        length = len(text)
        gap = int(self.width / length) if length > 0 else 0
        for x in range(length):
            point = [random.randint(x * gap, (x + 1) * gap),
                     random.randint(self.font.size, self.height - self.font.size)]
            if point[0] + self.font.size > self.width:
                point[0] = self.width - self.font.size
            # 随机生成颜色
            color = tuple([random.randint(0, 255) for x in range(4)])
            self.draw.text(
                tuple(point),
                text[x],
                fill=color,
                font=self.font)

    def _save(self, path=None, file_format="PNG"):
        if not self.draw:
            self._draw_text()
        if path:
            self.im.save(path, file_format)
        output = StringIO()
        self.im.save(output, file_format)
        self.data = output.getvalue()
        return self.data

    def gen(self, text, path=None):
        self.text = text
        file_format = "PNG"
        try:
            file_format = path.split(".")[-1].upper()
        except:
            pass
        if file_format == "PNG":
            self.im = Image.new(
                "RGBA", (self.width, self.height), self.background)
        else:
            self.im = Image.new(
                "RGB", (self.width, self.height), self.background)
        self._draw_text()
        return self._save(path, file_format)
    
    def show(self):
        try:
            self.im.show()
        except:
            print("Please call gen method first")

if __name__ == "__main__":
    i = ImageCaptcha()
    i.gen("123abc", "test.gif")