import random as rd
from read_files import data_dict
import numpy as np
import argparse as ap
import time
import csv
import os

def generate_coordinates(list_,m:int=200):

    array = np.zeros(m,dtype=np.int8)
    for ind in list_:
        array[int(ind)] = 1

    return array
    

def generate_instances(jlist,k:int=2,n:int=1000,max_:int=150):

    coordinates_dict = {}
    iter_max = n*10
    iter_ = 0
    len_dict = 0
    while len_dict < n:
        choices_ = rd.sample(jlist,k)
        #array_new = generate_coordinates(choices_,max_)
        in_list = False
        for key,array_ in coordinates_dict.items():
            bool_ = np.array_equal(array_,choices_)
            if bool_:
                in_list = True
                break
        
        if in_list == False:
            str_ = ','.join(choices_)
            coordinates_dict.update({str_:choices_})
            len_dict += 1

        iter_ += 1
        if iter_ > iter_max:
            break


    return coordinates_dict
    


if __name__ == '__main__':
    
    path = os.getcwd()
    foulder = os.path.join(path,'data')
    file1 = os.path.join(foulder,"courses.json")
    file2 = os.path.join(foulder,"jobs.json")
    file3 = os.path.join(foulder,"sfia.json")
    file4 = os.path.join(foulder,"units.json")
    
    files = [file1,file2,file3,file4]

    course,U,S,J = data_dict(files)

    list_jobs = list(J.keys())
    max_ = 0
    for ind in list_jobs:
        if int(ind) > max_:
            max_ = int(ind)


    n = 500
    list_instances = list_jobs.copy()
    for k in range(2,21):
        dict_ = generate_instances(list_jobs,k,n,max_)
        list_instances += list(dict_.keys())

    for key in list_instances:
        print(key)

    

    