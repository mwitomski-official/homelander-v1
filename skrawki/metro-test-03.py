'''
Pozyskanie rastrowej mapki ze strony oferty oraz próby odszukania interesujących nazw.
Celem jest ustalenie adresu wskazanego przez znacznik metrohouse
'''

import numpy as np
import requests
from bs4 import BeautifulSoup
import cv2
import pytesseract

test_link = r"https://metrohouse.pl/nieruchomosc/DUGA350/nieruchomosc-na-sprzedaz-mieszkanie-lodz-baluty-urzednicza"

r = requests.get(test_link)
soup = BeautifulSoup(r.text, 'html.parser')

map_link = soup.find('div', {'class': 'map-holder'})["style"]
map_link = map_link[map_link.find('(')+2: map_link.find(')')-1]
map_url = f"http://metrohouse.pl{map_link}"

img = requests.get(map_url, stream=True).raw
image = np.asarray(bytearray(img.read()), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)

cv2.imshow('Lokalizacja', image)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Perform edge detection
edges = cv2.Canny(gray, 100, 150, apertureSize=7)

# Find contours in the edge-detected image
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate through the contours
for contour in contours:
    # Ignore small contours
    if cv2.contourArea(contour) < 30:
        continue

    # Extract the bounding box of the contour
    x, y, w, h = cv2.boundingRect(contour)

    # Extract and crop the region of interest (ROI)
    roi = gray[y:y + h, x:x + w]

    # # Perform OCR on the cropped ROI
    # text = pytesseract.image_to_string(roi, config='--psm 6')
    #
    # # Print the extracted text
    # if text.strip() != "":
    #     print("Extracted Text:", text.strip())

    # Draw a rectangle around the detected area
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Show the result
cv2.imshow('Detected Text', image)

# Color Range method (powinno lepiej działać na HSV):
lower_color = np.array([20, 120, 50])
upper_color = np.array([110, 255, 255])

# Create a mask based on the color range
mask = cv2.inRange(image, lower_color, upper_color)

# Apply the mask to the original image
result = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow("Maska kolorów", result)


cv2.waitKey(0)
cv2.destroyAllWindows()