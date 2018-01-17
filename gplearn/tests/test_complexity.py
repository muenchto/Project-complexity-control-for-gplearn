"""Testing the Genetic Programming comlexity module."""

# Author: Tobias Münch and Gustavo Lorena>
#
#

from gplearn.complexity import complexity
import numpy as np

X_test = np.array([
    [5],
    [2],
    [9],
    [0],
    [7],
    [7],
])
y_test = np.array([
    1,
    5,
    7,
    8,
    4,
    0,
     ])
complexityarray = complexity(X_test, y_test)

X_test = np.array([
[0],
    [0],
    [1],
    [2],
[2],
])
y_test = np.array([
    0,
    0,
    1,
    0,
    0
])
complexityarray = complexity(X_test, y_test)



X_test = np.array([
    [0],
    [1],
    [2],
    [3],
    [4],
 ])
y_test = np.array([
    0,
    1,
    2,
    1,
    2,
 ])
complexityarray = complexity(X_test, y_test)

X_test = np.array([
    [0, 0],
    [1, 1],
    [2, 2],
    [3, 3],
    [4, 4],
 ])
y_test = np.array([
    0,
    1,
    2,
    1,
    2,
 ])
complexityarray = complexity(X_test, y_test)


X_test = np.array([
    [0, 5, 9],
    [1, 2, 1],
    [2, 8, 0],
 ])
y_test = np.array([
    0,
    1,
    2,
 ])
complexityarray = complexity(X_test, y_test)