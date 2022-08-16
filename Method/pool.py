#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
from multiprocessing import Pool

def isFaceInPointIdxList(inputs):
    face, point_idx_list = inputs
    return face.isInPointIdxList(point_idx_list)

def getFaceIdxListInPointIdxListWithPool(face_list, point_idx_list):
    inputs_list = [[face, point_idx_list] for face in face_list]
    pool = Pool(processes=os.cpu_count())
    result = pool.map(isFaceInPointIdxList, inputs_list)
    pool.close()
    face_idx_list = np.where(np.array(result) == True)[0].tolist()
    return face_idx_list

