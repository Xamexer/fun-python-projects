import math

rotation_angle = 0
centroid_point = 0
normalized_points = 0
resampled_points = 0
# Calculate Euclidean distance between two points
def path_length(points):
    d = 0
    for i in range(1, len(points)):
        d += distance(points[i-1], points[i])
    return d

def distance(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return math.sqrt(dx**2 + dy**2)

def resample(line, n):
    if n < 2 or len(line) < 2:
        raise ValueError("Invalid number of points or line coordinates.")

    resampled_line = [line[0]]  # Initialize with the first point
    total_length = path_length(line)
    segment_length = total_length / (n - 1)

    accumulated_length = 0
    current_segment = 1
    remaining_distance = segment_length

    for i in range(1, len(line)):
        segment = distance(line[i-1], line[i])

        while accumulated_length + segment >= current_segment * segment_length:
            ratio = (current_segment * segment_length - accumulated_length) / segment
            qx = line[i-1][0] + ratio * (line[i][0] - line[i-1][0])
            qy = line[i-1][1] + ratio * (line[i][1] - line[i-1][1])
            resampled_line.append((qx, qy))

            current_segment += 1

        accumulated_length += segment

    resampled_line.append(line[-1])

    return resampled_line[:n]


def centroid(points):
    n = len(points)
    cx = sum(p[0] for p in points) / n
    cy = sum(p[1] for p in points) / n
    return (cx, cy)


def rotate_by(points, angle):
    global centroid_point
    centroid_point = centroid(points)
    new_points = []
    for x, y in points:
        qx = (x - centroid_point[0]) * math.cos(angle) - (y - centroid_point[1]) * math.sin(angle) + centroid_point[0]
        qy = (x - centroid_point[0]) * math.sin(angle) + (y - centroid_point[1]) * math.cos(angle) + centroid_point[1]
        new_points.append((qx, qy))
    return new_points


def scale_to(points, size):
    min_x = min(points, key=lambda p: p[0])[0]
    min_y = min(points, key=lambda p: p[1])[1]
    max_x = max(points, key=lambda p: p[0])[0]
    max_y = max(points, key=lambda p: p[1])[1]
    scaled_points = []
    for x, y in points:
        qx = (x - min_x) * size / (max_x - min_x)
        qy = (y - min_y) * size / (max_y - min_y)
        scaled_points.append((qx, qy))
    return scaled_points


def path_distance(a, b):
    if len(a) != len(b):
        raise ValueError("Lists a and b must have the same length.")

    d = 0
    for i in range(len(a)):
        d += distance(a[i], b[i])
    return d / len(a)


def recognize(points, templates, size):
    global normalized_points
    global resampled_points
    global rotation_angle
    resampled_points = resample(points, 32)
    rotation_angle = -indicative_angle(resampled_points)
    rotated_points = rotate_by(resampled_points, rotation_angle)

    normalized_points = scale_to(rotated_points, size)

    best_score = float("inf")
    best_template = None

    for template in templates:
        d = distance_at_best_angle(normalized_points, template['points'], -45, 45, 2)
        #print(1 - d / (0.5 * math.sqrt(size ** 2 + size ** 2)), template['name'])
        if d < best_score:
            best_score = d
            best_template = template

    score = 1 - best_score / (0.5 * math.sqrt(size ** 2 + size ** 2))
    return best_template, score


def indicative_angle(points):
    centroid_point = centroid(points)
    return math.atan2(centroid_point[1] - points[0][1], centroid_point[0] - points[0][0])


def distance_at_best_angle(points, template_points, theta_a, theta_b, theta_delta):
    phi = 0.5 * (-1 + math.sqrt(5))
    x1 = phi * theta_a + (1 - phi) * theta_b
    f1 = distance_at_angle(points, template_points, x1)
    x2 = (1 - phi) * theta_a + phi * theta_b
    f2 = distance_at_angle(points, template_points, x2)

    while abs(theta_b - theta_a) > theta_delta:
        if f1 < f2:
            theta_b = x2
            x2 = x1
            f2 = f1
            x1 = phi * theta_a + (1 - phi) * theta_b
            f1 = distance_at_angle(points, template_points, x1)
        else:
            theta_a = x1
            x1 = x2
            f1 = f2
            x2 = (1 - phi) * theta_a + phi * theta_b
            f2 = distance_at_angle(points, template_points, x2)

    return min(f1, f2)


def distance_at_angle(points, template_points, theta):
    rotated_points = rotate_by(points, theta)
    return path_distance(rotated_points, template_points)

def preprocess_templates(templates, target_size=250):
    preprocessed_templates = []

    for template in templates:
        resampled_points = resample(template['points'], 32)
        rotation_angle = -indicative_angle(resampled_points)
        rotated_points = rotate_by(resampled_points, rotation_angle)
        scaled_points = scale_to(rotated_points, target_size)

        preprocessed_template = {
            'name': template['name'],
            'points': scaled_points
        }

        preprocessed_templates.append(preprocessed_template)
        #print(len(preprocessed_template['points']))

    return preprocessed_templates


# Example templates
template1 = {
    'name': 'Circle',
    'points': [
        (1.0, 0.0) ,
(0.9807852804032304, 0.19509032201612825) ,
(0.9238795325112867, 0.3826834323650898) ,
(0.8314696123025452, 0.5555702330196022) ,
(0.7071067811865476, 0.7071067811865475) ,
(0.5555702330196023, 0.8314696123025452) ,
(0.38268343236508984, 0.9238795325112867) ,
(0.19509032201612833, 0.9807852804032304) ,
(6.123233995736766e-17, 1.0) ,
(-0.1950903220161282, 0.9807852804032304) ,
(-0.3826834323650897, 0.9238795325112867) ,
(-0.555570233019602, 0.8314696123025455) ,
(-0.7071067811865475, 0.7071067811865476) ,
(-0.8314696123025453, 0.5555702330196022) ,
(-0.9238795325112867, 0.3826834323650899) ,
(-0.9807852804032304, 0.1950903220161286) ,
(-1.0, 1.2246467991473532e-16) ,
(-0.9807852804032304, -0.19509032201612836) ,
(-0.9238795325112868, -0.38268343236508967) ,
(-0.8314696123025455, -0.555570233019602) ,
(-0.7071067811865477, -0.7071067811865475) ,
(-0.5555702330196022, -0.8314696123025452) ,
(-0.38268343236509034, -0.9238795325112865) ,
(-0.19509032201612866, -0.9807852804032303) ,
(-1.8369701987210297e-16, -1.0) ,
(0.1950903220161283, -0.9807852804032304) ,
(0.38268343236509, -0.9238795325112866) ,
(0.5555702330196018, -0.8314696123025455) ,
(0.7071067811865474, -0.7071067811865477) ,
(0.8314696123025452, -0.5555702330196022) ,
(0.9238795325112865, -0.3826834323650904) ,
(0.9807852804032303, -0.19509032201612872)
    ]
}

template2 = {
    'name': 'Square',
    'points': [
        (100, 100),
        (200, 100),
        (200, 200),
        (100, 200),
        (100, 100)
    ]
}

template3 = {
    'name': 'Triangle',
    'points': [
        (100, 100),
        (150, 200),
        (200, 100),
        (100, 100)
    ]
}
template4 = {'name': 'Circle',
             'points':
                 [(0.9807852804032303, -0.19509032201612872),
                  (0.9238795325112865, -0.3826834323650904),
                  (0.8314696123025452, -0.5555702330196022),
                  (0.7071067811865474, -0.7071067811865477),
                  (0.5555702330196018, -0.8314696123025455),
                  (0.38268343236509, -0.9238795325112866),
                  (0.1950903220161283, -0.9807852804032304),
                  (-1.8369701987210297e-16, -1.0),
                  (-0.19509032201612866, -0.9807852804032303),
                  (-0.38268343236509034, -0.9238795325112865),
                  (-0.5555702330196022, -0.8314696123025452),
                  (-0.7071067811865477, -0.7071067811865475),
                  (-0.8314696123025455, -0.555570233019602),
                  (-0.9238795325112868, -0.38268343236508967),
                  (-0.9807852804032304, -0.19509032201612836),
                  (-1.0, 1.2246467991473532e-16),
                  (-0.9807852804032304, 0.1950903220161286),
                  (-0.9238795325112867, 0.3826834323650899),
                  (-0.8314696123025453, 0.5555702330196022),
                  (-0.7071067811865475, 0.7071067811865476),
                  (-0.555570233019602, 0.8314696123025455),
                  (-0.3826834323650897, 0.9238795325112867),
                  (-0.1950903220161282, 0.9807852804032304),
                  (6.123233995736766e-17, 1.0),
                  (0.19509032201612833, 0.9807852804032304),
                  (0.38268343236508984, 0.9238795325112867),
                  (0.5555702330196023, 0.8314696123025452),
                  (0.7071067811865476, 0.7071067811865475),
                  (0.8314696123025452, 0.5555702330196022),
                  (0.9238795325112867, 0.3826834323650898),
                  (0.9807852804032304, 0.19509032201612825),
                  (1.0, 0.0)
                  ]
             }

template5 = {'name': 'Square',
             'points': [
                 (100, 100),
                 (100, 200),
                 (200, 200),
                 (200, 100),
                 (100, 100)
             ]
             }
template6 = {'name': 'Triangle',
             'points': [
                 (100, 100),
                 (200, 100),
                 (150, 200),
                 (100, 100)
             ]
             }


gesture1 = [
    (120, 120),
    (130, 120),
    (140, 130),
    (140, 140),
    (130, 150),
    (120, 150),
    (110, 140),
    (110, 130),
    (120, 120)
]


templates = [template1, template2, template3, template4, template5, template6]

# Preprocess the templates
preprocessed_templates = preprocess_templates(templates)
#for template in preprocessed_templates:
 #   print(len(template['points']))
# Test the recognition algorithm
#best_template, score = recognize(gesture1, [{'name': template1['name'], 'points': scaled_template}], 250)
#best_template, score = recognize(gesture1, preprocessed_templates, 250)


# Print the result
#print("Recognized Gesture:", best_template['name'])
#print("Recognition Score:", score)
