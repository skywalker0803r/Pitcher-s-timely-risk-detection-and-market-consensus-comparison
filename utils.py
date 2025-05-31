import numpy as np

def get_landmark_vector(lm, index):
    if isinstance(lm, list):
        return np.array([[frame[index].x, frame[index].y, frame[index].z] for frame in lm])
    else:
        return np.array([lm[index].x, lm[index].y, lm[index].z])


def calculate_angle(a, b, c):
    def calculate_angle_single_frame(a, b, c):
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
        return np.degrees(angle)
    if a.ndim == 2 and b.ndim == 2 and c.ndim == 2:
        return np.array([calculate_angle_single_frame(a[i], b[i], c[i]) for i in range(len(a))])
    else:
        return calculate_angle_single_frame(a, b, c)
