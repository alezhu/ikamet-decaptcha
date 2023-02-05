from pathlib import Path
import pytesseract
from typing import IO
from PIL import Image, ImageFilter



def crop_by_main_color(image: Image, main_color: int, margin: int = 3) -> Image:
    size = image.size
    width = size[0]
    height = size[1]
    xCount = [0] * width
    yCount = [0] * height
    for x in range(width):
        for y in range(height):
            px = image.getpixel((x, y))
            if px == main_color:
                xCount[x] = xCount[x] + 1
                yCount[y] = yCount[y] + 1
    left = 0
    right = width
    top = 0
    bottom = height
    for x in range(width):
        left = x
        if xCount[x] > 2:
            break
    for x in range(width - 1, left, -1):
        right = x
        if xCount[x] > 2:
            break

    for y in range(height):
        top = y
        if yCount[y] > 10:
            break
    for y in range(top, height):
        bottom = y
        if yCount[y] < 10:
            break

    left = max([0, left - margin])
    right = min([width, right + margin])
    top = max([0, top - margin])
    bottom = min([height, bottom + margin])
    result: Image = image.crop((left, top, right, bottom))
    return result


def is_square(image: Image, x: int, y: int, noise_colors: list[int], min_threshold = 3) -> bool:
    # pixels4 = [0] * 4
    count = 0
    for dx in range(2):
        for dy in range(2):
            pixel = image.getpixel((x + dx, y + dy))
            # pixels4[dx * 2 + dy] = pixel
            count += 1 * pixel in noise_colors
    return count >= min_threshold

def fill_square(image: Image, x: int, y: int, main_color: int) -> None:
    for dx in range(2):
        for dy in range(2):
            image.putpixel((x + dx, y + dy),main_color)


def unsquare1(image: Image, noise_color: int, main_color: int,  min_threshold = 3) -> None:
    size = image.size
    width = size[0]
    height = size[1]
    pallete = image.palette
    colors = pallete.colors
    noise_colors = [noise_color]

    for x in range(width - 1):
        for y in range(height - 1):
            if is_square(image,x,y,noise_colors,min_threshold):
                fill_square(image,x,y,main_color)

def unsquare2(image: Image, noise_color: int, main_color: int, min_threshold = 3) -> None:
    size = image.size
    width = size[0]
    height = size[1]
    pallete = image.palette
    colors = pallete.colors
    noise_colors = [noise_color]
    for noise_rgb in [(255, 213, 204), (204, 255, 255), (204, 255, 204), (255, 213, 255), (204, 213, 255)]:
        noise_color = colors[noise_rgb]
        if (noise_color):
            noise_colors.append(noise_color)

    for x in range(width - 1):
        for y in range(height - 1):
            if is_square(image,x,y,noise_colors,min_threshold):
                fill_square(image,x,y,main_color)

def noise_reduction(image: Image, noise_color: int, main_color: int, bg_color: int) -> None:
    size = image.size
    width = size[0]
    height = size[1]
    for x in range(width):
        for y in range(height):
            px = image.getpixel((x, y))
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                if px != bg_color:
                    image.putpixel((x,y),bg_color)
            else:
                if px  == noise_color: #!= main_color and px != bg_color:
                    count = 0
                    for dx in range(x-1,x+2):
                        for dy in range(y-1,y+2):
                            px =image.getpixel((dx,dy))
                            if px == main_color:
                                count += 1
                    if count < 5:
                        image.putpixel((x,y),bg_color)
                    else:
                        image.putpixel((x,y),main_color)

def filter_median(image: Image ) -> Image:
    temp = image.convert("RGB")
    result = temp.filter(ImageFilter.MedianFilter(3))
    # result = temp.convert("P",None,Image.Dither.NONE,Image.Palette.ADAPTIVE )
    return result



def process(file:str | bytes | Path | IO[bytes])->str:
    with Image.open(file) as image:
        pallete = image.palette
        colors = pallete.colors
        clBlue = colors[(0, 0, 255)]
        clWhite = colors[(255, 255, 255)]

        clNoise = image.getpixel((0, 0))

        with crop_by_main_color(image, clBlue) as image2:
            unsquare1(image2,clNoise,clBlue,4)
            unsquare2(image2,clNoise,clBlue,4)
            unsquare1(image2,clNoise,clBlue,3)
            unsquare2(image2,clNoise,clBlue,3)
            noise_reduction(image2,clNoise,clBlue,clWhite)
            with filter_median(image2) as image3:
                image4 = Image.new("RGB",(image.width,image.height),(255,255,255))
                image4.paste(image3,((image4.width - image3.width) >> 1, (image4.height - image3.height) >> 1 ) )
                result = pytesseract.image_to_string(image4) 

    return result
