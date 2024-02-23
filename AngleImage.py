from PIL import Image, ImageFilter
from math import acos, degrees

def erode(cycles, image):
    for _ in range(cycles):
         image = image.filter(ImageFilter.MinFilter(3))
    return image

imgRotated = Image.open("Example4.png")
imgGray = imgRotated.convert("L")
imgGray = imgGray.filter(ImageFilter.SHARPEN)
threshold = 50

imgThreshold = imgGray.point(
    lambda x: 255 if x > threshold else 0
)

imgGray = imgGray.filter(ImageFilter.CONTOUR)
imgGray = imgGray.convert("1")
imgGray = erode(1, imgGray)

pixels = imgGray.load()
width, height = imgGray.size
pixels = [[pixels[j, i] for j in range(width)] for i in range(height)]
passed = [[0 for _ in range(width)] for _ in range(height)]

xStart = 0
yStart = 0
xNow = 0
yNow = 0
maxLength = 0
angle = 0

for i in range(1, height - 1):
    for j in range(1, width - 1):
        if pixels[i][j] == 0 and pixels[i - 1][j] != 0 and passed[i][j] == 0:
            xStart = xNow = j
            yStart = yNow = i

            while (yNow < height - 1 and xNow < width - 1):
                if pixels[yNow][xNow + 1] == 0 and pixels[yNow - 1][xNow + 1] != 0 and passed[yNow][xNow + 1] == 0:
                    xNow += 1
                elif pixels[yNow + 1][xNow] == 0 and pixels[yNow][xNow + 1] != 0 and passed[yNow][xNow + 1] == 0:
                    yNow += 1
                else:
                    break
                
                passed[yNow][xNow] = 1

            if maxLength < (length := ((xNow - xStart) ** 2 + (yNow - yStart) ** 2) ** 0.5):
                maxLength = length
                angle = degrees(acos((xNow - xStart) / length))

            xStart = xNow = j
            yStart = yNow = i

            while (yNow < height - 1 and xNow > 1):
                if pixels[yNow][xNow - 1] == 0 and pixels[yNow - 1][xNow - 1] != 0 and passed[yNow][xNow - 1] == 0:
                    xNow -= 1
                elif pixels[yNow + 1][xNow] == 0 and pixels[yNow][xNow - 1] != 0 and passed[yNow][xNow - 1] == 0:
                    yNow += 1
                else:
                    break
                
                passed[yNow][xNow] = 1

            if maxLength < (length := ((xNow - xStart) ** 2 + (yNow - yStart) ** 2) ** 0.5):
                maxLength = length
                angle = -degrees(acos((xStart - xNow) / length))

print("Angle:", angle)

imgRotated.rotate(angle, expand=True, fillcolor="white").save("Example_Result.png")