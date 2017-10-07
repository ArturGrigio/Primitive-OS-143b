from __future__ import print_function

import json
import math
from . import lib
from . import numpy

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    # print(event['key1'])
    # print(event['key2'])
    # print(event['key3'])
    matrix = buildMatrix(event)
    transposed = transpose(matrix)
    print(matrix)
    print(transposed)
    # return event['key1']  # Echo back the first key value
    #raise Exception('Something went wrong')


def buildMatrix(jsonMatrix):
    rows = len(jsonMatrix)
    cols = len(jsonMatrix[0])
    matrix = [[0 for j in range(cols)] for i in range(rows)]

    for row in jsonMatrix:
        for col in jsonMatrix[row]:
            matrix[row][col] = jsonMatrix[row][col]
    return matrix


def transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    transposed = [[0 for j in range(rows)] for i in range(cols)]

    for row in range(rows):
        for col in range(cols):
            transposed[col][row] = matrix[row][col]
    return transposed


lambda_handler({0:{0: 1, 1: 2, 2: 3},1:{0: 1, 1: 2, 2: 3}}, None)