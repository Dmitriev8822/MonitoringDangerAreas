import os
from ultralytics import YOLO
from shapely.geometry import Polygon
import cv2
import numpy as np

def generate_video(path_for_video,polygon_path):
	with open(polygon_path, 'r') as file:
	    content = file.read()

	
	raw_data = content.replace('[', '').replace(']', '').split(',')
	
	polygon_coords = [list(map(int, raw_data[i:i+2])) for i in range(0, len(raw_data), 2)]


	print(polygon_coords)
	# polygon_coords = [[718, 204],
	#           [1128, 340],
	#           [1128, 720],
	#           [541, 720],
	#           [345, 607]
	#           ]

	pts = np.array(polygon_coords, np.int32)
	pts = pts.reshape((-1, 1, 2))

	video_path = (path_for_video)

	model_path = os.path.join('.', 'runs', 'detect', 'train2', 'weights', 'last.pt')

	model = YOLO(model_path)

	threshold = 0.1

	cap = cv2.VideoCapture(video_path)

	while True:
	    ret, frame = cap.read()
	    if not ret:
	        break

	    results = model(frame)[0]

	    cv2.polylines(frame, [pts], True, (255, 0, 0), thickness=2)

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
	                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
	            else:
	                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)

	    cv2.imshow('frame', frame)
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

	cap.release()
	cv2.destroyAllWindows()
