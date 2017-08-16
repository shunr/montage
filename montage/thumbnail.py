from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def generate_thumbnail(img_path, text):
    img = Image.open(img_path)
    font_size = int(img.width / len(text))
    border = int(img.width * 0.02)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./resources/font.ttf", font_size)

    w, h = draw.textsize(text, font=font)

    #draw.text(((img.width - w) / 2, 0), text, (255, 255, 255), font=font)

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 64))
    bordered_img = Image.new("RGB", img.size, (255, 255, 255))

    img = Image.alpha_composite(img, overlay)

    img = img.crop(
        (
            border,
            border,
            img.width - border,
            img.height - border
        )
    )

    bordered_img.paste(img, (border, border))

    bordered_img.save('sample-out.png')
