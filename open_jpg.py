import os
from ultralytics import YOLO
from shapely.geometry import Polygon
import cv2
import numpy as np

polygon_coords = [[534, 288],
                  [834, 219],
                  [1365, 580],
                  [1124, 806]
                  ]
pts = np.array(polygon_coords, np.int32)
pts = pts.reshape((-1, 1, 2))

image_path = os.path.join('MT/test3.jpg')
model_path = os.path.join('.', 'runs', 'detect', 'train', 'weights', 'last.pt')
model = YOLO(model_path)

threshold = 0.1

image = cv2.imread(image_path)

results = model(image)[0]

cv2.polylines(image, [pts], True, (255, 0, 0), thickness=2)

for result in results.boxes.data.tolist():
    x1, y1, x2, y2, score, class_id = result
    if score > threshold:
        rectangle_coords = [[x1, y1], [x1, y2], [x2, y2], [x2, y1]]
        polygon = Polygon(polygon_coords)
        rectangle = Polygon(rectangle_coords)
        intersection = rectangle.intersection(polygon)
        intersection_area = intersection.area
        rectangle_area = rectangle.area
        if rectangle_area != 0 and int((intersection_area / rectangle_area) * 100) >= 15:
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
        else:
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)

# Показываем изображение
cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
