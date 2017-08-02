#coding:utf-8
from random import randint, choice
from PIL import Image, ImageDraw, ImageFont
from cStringIO import StringIO
from string import printable


def pillow_test():
    font_path = "utills/captcha/font/Arial.ttf"
    # img = Image.open('files/upload_files/222.png')
    # out = StringIO()
    # img.save(out, format='jpeg')
    # content = out.getvalue()
    # out.close()
    # return content
    font_color = (randint(150, 200), randint(0, 150), randint(0, 150))
    line_color = (randint(0, 150), randint(0, 150), randint(150, 200))
    point_color = (randint(0, 150), randint(100, 150), randint(150, 200))

    width, height = 100, 40
    image = Image.new('RGB', (width, height), (200, 200, 200))
    font = ImageFont.truetype(font_path, height-10)
    draw = ImageDraw.Draw(image)

    #生成验证码
    text = ''.join([choice(printable[:62]) for i in xrange(4)])
    font_width, font_height = font.getsize(text)
    #把验证码写到画布上
    draw.text((10, 10), text, font = font, fill=font_color)
    #绘制线条
    for i in xrange(0, 5):
        draw.line(((randint(0, width), randint(0, height)), (randint(0, width), randint(0, height))),
                  fill=line_color, width=2)
    #绘制点
    for i in xrange(randint(100, 1000)):
        draw.point((randint(0, width), randint(0, height)), fill=point_color)

    #输出
    out = StringIO()
    image.save(out, format='jpeg')
    content = out.getvalue()
    out.close()
    return text, content
    print content
    print '-'*80