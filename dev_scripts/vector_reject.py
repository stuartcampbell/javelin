import numpy as np
from random import random


def gutmann(s, q):
    return np.cross(np.cross(q, s), q)/np.dot(q, q)


def reject(s, q):
    return s - np.dot(s, q)/np.dot(q, q)*q


q1 = np.array([1, 0, 0])
s = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0])


while True:
    q = np.array([random(), random(), random()])
    s = np.array([random(), random(), random()])
    x = gutmann(s, q)
    y = reject(s, q)
    if (x != y).any():
        print(q, s, x, y)
