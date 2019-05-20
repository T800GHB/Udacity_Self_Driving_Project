#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 08:34:44 2019

@author: hbguo
"""
import numpy as np

class object_info(object):
    def __init__(self, up=10000, left=10000, down=0, right=0, area=0, thin=0):
        '''constructer'''
        self.__up = up
        self.__left = left
        self.__down = down
        self.__right = right
        self.__area = area
        self.__thin = thin

    @property
    def up(self):
        return self.__up

    @up.setter
    def up(self, up):
        if up < 0:
            raise ValueError('Location in image should not less than 0')
        self.__up = up

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, left):
        if left < 0:
            raise ValueError('Location in image should not less than 0')
        self.__left = left

    @property
    def down(self):
        return self.__down

    @down.setter
    def down(self, down):
        if down < 0:
            raise ValueError('Location in image should not less than 0')
        self.__down = down

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, right):
        if right < 0:
            raise ValueError('Location in iamge should not less than 0')
        self.__right = right

    @property
    def area(self):
        return self.__area

    @area.setter
    def area(self, area):
        if area < 0:
            raise ValueError('Area calculation failure')
        elif area == 0:
            self.__area = 1
        else:
            self.__area = area
            
    @property
    def thin(self):
        return self.__thin
    @thin.setter
    def thin(self, thin):
        if thin < 0:
            raise ValueError('Thin calculation failure')
        elif thin == 0:
            self.__thin = 1
        else:
            self.__thin = thin
            
    @property
    def width(self):
        if self.__right < self.__left:
            return 0
        else:
            return self.__right - self.__left + 1

    @property
    def height(self):
        if self.__down < self.__up:
            return 0
        else:
            return self.__down - self.__up + 1


def connection_label(bindata, thr=50, direction=8, thin_thre=15):
    '''
    This function will find a set of connection regions.
    Parameter of input is: threshold used for getting binary image,
    number of connection adjacent pixel(4 or 8)
    run block means a independent foreground piexls set in a row.
    '''
    height = bindata.shape[0]
    width = bindata.shape[1]

    '''
    Establish a container to store a set of indices that indicate start and end
    foreground pixel in its row.
    Because of unknow quantity should be recoreded, so list will be more convenient.
    '''
    run_start = []
    run_end = []
    '''Record the rows that run block belonging'''
    run_row = []
    '''Last index in a row'''
    border = width - 1
    '''Scan the full image to record run block'''
    for i in range(height):
        '''First element in this row is foreground pixel'''
        if bindata[i, 0]:
            run_row.append(i)
            run_start.append(0)
        for j in range(1, width):
            '''Find b-f switch location that will be treated as start index'''
            if (not bindata[i, j - 1]) and bindata[i, j]:
                run_row.append(i)
                run_start.append(j)
            '''Record run block end index'''
            if bindata[i, j - 1] and (not bindata[i, j]):
                run_end.append(j - 1)
            '''Maybe the end index is the last one in this row'''
            if bindata[i, j] and j == border:
                run_end.append(border)
    assert (len(run_row) == len(run_start) == len(run_end)), \
        'Recoud unequal %d, %d, %d' % (len(run_row), len(run_start), len(run_end))
    run_count = len((run_start))
    '''
    Establish container to record run block label.
    This array will be used as indices, so int data type needed.
    '''
    run_label = np.zeros(run_count, dtype=int)
    '''Record pairs of equal label, unknow quantity, use list'''
    label_pair = []
    '''Assistant index to help scan run block record'''
    per_start = 0  # Indicate the start index in perious row
    per_end = 0  # Indicate the end index in preious row
    cur_index = 0  # Record the row that is scanning
    label_value = 1  # Label generator
    '''Set the number of adjcent pixel that belong to same connection region'''
    if direction == 8:
        offset = 1
    elif direction == 4:
        offset = 0
    else:
        raise ValueError('Connection parameter setting limited only 4 or 8')
    '''
    Scanning run block record and assign labels to the unlabel ones.
    If run block in adjacent two rows overlaped with columns, use same label.
    If the overlaped ones already have different labels, record as equal pair
    '''
    for i in range(run_count):
        '''Update index information, when the current row has scanned.'''
        if cur_index != run_row[i]:
            cur_index = run_row[i]
            per_start = per_end
            per_end = i
        '''Search overlap'''
        for j in range(per_start, per_end):
            if ((run_start[i] <= run_end[j] + offset)
                and (run_start[j] <= run_end[i] + offset)
                and (run_row[j] + 1 == run_row[i])):
                if run_label[i] == 0:
                    run_label[i] = run_label[j]
                elif (run_label[i] != 0 and run_label[i] != run_label[j]):
                    label_pair.append([run_label[i], run_label[j]])
        '''If this run block does not overlap with other, assign a new label'''
        if run_label[i] == 0:
            run_label[i] = label_value
            label_value += 1
    pair_count = len(label_pair)  # Total number of equal pair
    '''Delete repeat element in equal pair record'''
    for i in range(1, pair_count):
        for j in range(i):
            if label_pair[j][0] != 0:
                if ((label_pair[j][0] == label_pair[i][0]
                     and label_pair[j][1] == label_pair[i][1])
                    or
                        (label_pair[j][0] == label_pair[i][1]
                         and label_pair[j][1] == label_pair[i][0])):
                    label_pair[i][0] = 0  # Set to zeros as one wait for deleting
    '''Unique operation, delete all repeat elements and move unique ones to head.'''
    head = 0  # receive pointer
    search = 0  # Send pointer
    while search < pair_count:
        if label_pair[search][0] != 0:
            if head == search:
                head += 1
                search += 1
            else:
                label_pair[head][0] = label_pair[search][0]
                label_pair[head][1] = label_pair[search][1]
                head += 1
                search += 1
        else:
            search += 1

    '''Reset total number of equal pair'''
    pair_count = head

    '''
    Merge equal pair.
    Equal pair record just like a graph that stored as sparse matrix.
    So we need to search all the connection relationship from one node ,
    and  assign them a same label.
    '''
    label_flag = np.zeros(label_value, dtype=int)  # Table of label mapping to new one
    new_label = 0  # New label

    for i in range(1, label_value):
        if label_flag[i] != 0:
            continue
        '''New relationship created'''
        new_label += 1
        label_flag[i] = new_label
        '''Establish temporary list to store connection relationship'''
        temp_list = []
        temp_list.append(i)
        index = 0
        while index < len(temp_list):
            for pair in label_pair:
                if pair[0] == temp_list[index]:
                    equal_com = pair[1]  # Equal pair another component
                    if label_flag[equal_com] == 0:
                        temp_list.append(equal_com)  # Add new connection
                        label_flag[equal_com] = new_label  # Assign new label
                if pair[1] == temp_list[index]:
                    equal_com = pair[0]
                    if label_flag[equal_com] == 0:
                        temp_list.append(equal_com)
                        label_flag[equal_com] = new_label
            index += 1

    '''
    Mapping orignal label of run block to new one.
    At this time, 0 could be used as label.
    In the previous procedure, 0 was used as empty or invalid flag.
    '''
    for i in range(run_count):
        run_label[i] = label_flag[run_label[i]] - 1

    '''Create a list with object_info class'''
    object_set = [object_info() for i in range(new_label)]

    '''Achive connection labeled object information'''
    for i in range(run_count):
        index = run_label[i]
        if run_start[i] < object_set[index].left:
            object_set[index].left = run_start[i]
        if object_set[index].right < run_end[i]:
            object_set[index].right = run_end[i]
        if run_row[i] < object_set[index].up:
            object_set[index].up = run_row[i]
        if object_set[index].down < run_row[i]:
            object_set[index].down = run_row[i]
        if object_set[index].thin < (run_end[i] - run_start[i]):
            object_set[index].thin = (run_end[i] - run_start[i])
        object_set[index].area += run_end[i] - run_start[i] + 1
        
    del_list = []
    for i, obj in enumerate(object_set):
        if obj.area < thr:
            del_list.append(i)
        if obj.thin < thin_thre:
            del_list.append(i)

    run_count = len(run_row)
    for i in range(run_count):
        if run_label[i] in del_list:
            for j in range(run_start[i], run_end[i] + 1):
                bindata[run_row[i], j] = 0
    return bindata