# -*- coding: utf-8 -*-
"""
Author: Roger X. Lera Leri
Date: 30/09/2023
"""
from definitions import *
from matrices import array_creation
from read_files import data_dict
import cplex as cp
import numpy as np
import argparse as ap
import time
import csv
import os
from docplex.mp.model import Model


def constraints(matrices,c_T,mdl,variables):

    L,x_keys,B,P,C,D,d,R,or_,r,E,F,f,G,g,t,A,K,keys_ = matrices
    
    keys = list(x_keys.keys())
    x,v,y,z,zl = variables 
    # defining constraints
    len_v = np.shape(f)[1]
    len_y = np.shape(A)[0]
    len_z = np.shape(K)[0]
    Delta = len(x_keys)

    constraints_keys = {}
    counter = 0
    
    # Bx <= 1
    mdl.add_constraints(mdl.sum(B[i,j]*x[j] for j in range(len(keys))) <= 1
                   for i in range(np.shape(B)[0]))
    for i in range(np.shape(B)[0]):
        constraints_keys.update({counter:f"b{i}"})
        counter += 1
    # Px == 0
    mdl.add_constraints(mdl.sum(P[i,j]*x[j] for j in range(len(keys))) == 0
                   for i in range(np.shape(P)[0]))
    for i in range(np.shape(P)[0]):
        constraints_keys.update({counter:f"p{i}"})
        counter += 1

    # Dx == d
    mdl.add_constraints(mdl.sum(D[i,j]*x[j] for j in range(len(keys))) == d[i]
                   for i in range(np.shape(D)[0]))
    for i in range(np.shape(D)[0]):
        constraints_keys.update({counter:f"d{i}"})
        counter += 1
    # Rx >= rx
    mdl.add_constraints(mdl.sum(R[i,j]*x[j] for j in range(len(keys))) >= mdl.sum(r[i,k]*x[k] for k in range(len(keys)))
                   for i in range(np.shape(R)[0]))
    for i in range(np.shape(R)[0]):
        constraints_keys.update({counter:f"r{i}"})
        counter += 1
    # Ex == 1
    mdl.add_constraints(mdl.sum(E[i,j]*x[j] for j in range(len(keys))) == 1
                   for i in range(np.shape(E)[0]))
    for i in range(np.shape(E)[0]):
        constraints_keys.update({counter:f"e{i}"})
        counter += 1
    # 1v >= 1
    mdl.add_constraint(mdl.sum(v[j] for j in range(len_v)) >= 1)
    constraints_keys.update({counter:f"v"})
    counter += 1
    # Fx >= fv
    mdl.add_constraints(mdl.sum(F[i,j]*x[j] for j in range(len(keys))) >= mdl.sum(f[i,k]*v[k] for k in range(len_v))
                   for i in range(np.shape(F)[0]))
    for i in range(np.shape(F)[0]):
        constraints_keys.update({counter:f"f{i}"})
        counter += 1
    # Gx >= gv
    mdl.add_constraints(mdl.sum(G[i,j]*x[j] for j in range(len(keys))) >= mdl.sum(g[i,k]*v[k] for k in range(len_v))
                   for i in range(np.shape(G)[0]))
    for i in range(np.shape(G)[0]):
        constraints_keys.update({counter:f"g{i}"})
        counter += 1
    # Ax <= Delta y
    mdl.add_constraints(mdl.sum(A[i,j]*x[j] for j in range(len(keys))) <= Delta*y[i]
                   for i in range(np.shape(A)[0]))
    for i in range(np.shape(A)[0]):
        constraints_keys.update({counter:f"a{i}"})
        counter += 1
    # Ax >= Delta (y-1) + 1
    mdl.add_constraints(mdl.sum(A[i,j]*x[j] for j in range(len(keys))) >= Delta*(y[i]-1) + 1
                   for i in range(np.shape(A)[0]))
    for i in range(np.shape(A)[0]):
        constraints_keys.update({counter:f"a{i}"})
        counter += 1
    # z <= Ky - t
    mdl.add_constraints( z[i] <= mdl.sum(K[i,j]*y[j] for j in range(len_y)) - t[i]
                   for i in range(len_z))
    for i in range(np.shape(K)[0]):
        constraints_keys.update({counter:f"k{i}"})
        counter += 1
    # z <= 0
    mdl.add_constraints(z[i] <= 0 for i in range(len_z))
    for i in range(np.shape(K)[0]):
        constraints_keys.update({counter:f"k{i}"})
        counter += 1
    # -zl <= z
    mdl.add_constraints( - zl[i] <= z[i] for i in range(len_z))
    for i in range(np.shape(K)[0]):
        constraints_keys.update({counter:f"k{i}"})
        counter += 1
    # z <= zl
    mdl.add_constraints(z[i] <= zl[i] for i in range(len_z))
    for i in range(np.shape(K)[0]):
        constraints_keys.update({counter:f"k{i}"})
        counter += 1
    
    return constraints_keys


def constraints_cp(matrices,c_T,mdl,variables):

    L,x_keys,B,P,C,D,d,R,or_,r,E,F,f,G,g,t,A,K,keys_ = matrices
    
    keys = list(x_keys.keys())
    x,v = variables 
    # defining constraints
    len_v = np.shape(f)[1]

    constraints_keys = {}
    counter = 0
    
    # Bx <= 1
    mdl.add_constraints(mdl.sum(B[i,j]*x[j] for j in range(len(keys))) <= 1
                   for i in range(np.shape(B)[0]))
    for i in range(np.shape(B)[0]):
        constraints_keys.update({counter:f"b{i}"})
        counter += 1
    # Px == 0
    mdl.add_constraints(mdl.sum(P[i,j]*x[j] for j in range(len(keys))) == 0
                   for i in range(np.shape(P)[0]))
    for i in range(np.shape(P)[0]):
        constraints_keys.update({counter:f"p{i}"})
        counter += 1

    # Dx == d
    mdl.add_constraints(mdl.sum(D[i,j]*x[j] for j in range(len(keys))) == d[i]
                   for i in range(np.shape(D)[0]))
    for i in range(np.shape(D)[0]):
        constraints_keys.update({counter:f"d{i}"})
        counter += 1
    # Rx >= rx
    mdl.add_constraints(mdl.sum(R[i,j]*x[j] for j in range(len(keys))) >= mdl.sum(r[i,k]*x[k] for k in range(len(keys)))
                   for i in range(np.shape(R)[0]))
    for i in range(np.shape(R)[0]):
        constraints_keys.update({counter:f"r{i}"})
        counter += 1
    # Ex == 1
    mdl.add_constraints(mdl.sum(E[i,j]*x[j] for j in range(len(keys))) == 1
                   for i in range(np.shape(E)[0]))
    for i in range(np.shape(E)[0]):
        constraints_keys.update({counter:f"e{i}"})
        counter += 1
    # 1v >= 1
    mdl.add_constraint(mdl.sum(v[j] for j in range(len_v)) >= 1)
    constraints_keys.update({counter:f"v"})
    counter += 1
    # Fx >= fv
    mdl.add_constraints(mdl.sum(F[i,j]*x[j] for j in range(len(keys))) >= mdl.sum(f[i,k]*v[k] for k in range(len_v))
                   for i in range(np.shape(F)[0]))
    for i in range(np.shape(F)[0]):
        constraints_keys.update({counter:f"f{i}"})
        counter += 1
    # Gx >= gv
    mdl.add_constraints(mdl.sum(G[i,j]*x[j] for j in range(len(keys))) >= mdl.sum(g[i,k]*v[k] for k in range(len_v))
                   for i in range(np.shape(G)[0]))
    for i in range(np.shape(G)[0]):
        constraints_keys.update({counter:f"g{i}"})
        counter += 1

    return constraints_keys



def model_cplex(matrices,c_T):

    s_time = time.time()
    L,x_keys,B,P,C,D,d,R,or_,r,E,F,f,G,g,t,A,K,keys_ = matrices

    # creating the model
    keys = list(x_keys.keys())
    mdl = Model()

    # defining variables
    x = mdl.binary_var_dict(keys)
    len_v = np.shape(f)[1]
    v = mdl.binary_var_list(len_v,name='v')
    len_y = np.shape(A)[0]
    y = mdl.binary_var_list(len_y,name='y')
    len_z = np.shape(K)[0]
    z = mdl.integer_var_list(len_z,lb=-7,name='z')
    zl = mdl.integer_var_list(len_z,name='zl')
    variables = x,v,y,z,zl

    constraint_keys = constraints(matrices,c_T,mdl,variables)
    
    # cost function
    mdl.minimize(mdl.sum(zl[i] for i in range(len_z)))

    model_time = time.time() - s_time

    return mdl,variables,constraint_keys,model_time


def model_cp(matrices,c_T,S):

    s_time = time.time()
    L,x_keys,B,P,C,D,d,R,or_,r,E,F,f,G,g,t,A,K,keys_ = matrices

    # creating the model
    keys = list(x_keys.keys())
    mdl = Model()

    # defining variables
    x = mdl.binary_var_dict(keys)
    len_v = np.shape(f)[1]
    v = mdl.binary_var_list(len_v,name='v')
    variables = x,v

    constraint_keys = constraints_cp(matrices,c_T,mdl,variables)
    skill_units_matrix = []
    for i in range(len(S.keys())):
        skill_row = []
        skill_id = list(S.keys())[i]
        for j,var_e in x_keys.items():
            unit = var_e[0]
            sem = var_e[1]
            skill_lev = 0
            for skill2 in unit.skills:
                if skill2.id == skill_id:
                    skill_lev = skill2.level
                    break
            skill_row.append(skill_lev)
        skill_units_matrix.append(skill_row)
    # cost function
    mdl.minimize(mdl.sum(mdl.abs(mdl.min([mdl.max(skill_units_matrix[i][j]*x[j] for j in range(len(keys)))-t[i],0])) for i in range(len(S.keys()))))

    model_time = time.time() - s_time

    return mdl,variables,constraint_keys,model_time,skill_units_matrix


def solve_model(model,x,x_keys,cp=False):
    
    #model.print_information()
    #model.export_as_lp(f'cplex_{cp}.lp')
    model.solve(log_output=False)
    #model.report()
    f_ = model.objective_value

    assignments = {}
    for i in x_keys.keys():
        if x[i].solution_value > 0.5:
            unit = x_keys[i][0]
            l = x_keys[i][1]
            assignments.update({i:(unit,l)})

    return assignments,f_,model.solve_details.time

def print_plan(assignments,L):

    print('****************************************')
    print('***************** PLAN *****************')
    print('****************************************')
    print()
    print("------------------------------------")
    for l in L.keys():
        l_ob = L[l]
        print(f"SEMESTER: {l_ob.id}")
        for i in assignments.keys():
            u_a = assignments[i][0]
            l_a = assignments[i][1]
            if l_ob.id == l_a.id:
                print(f"\t {u_a.name}")

        print("------------------------------------")


    return None

def z_vec(x,x_keys,S,matrix_sv):

    z = []
    for i in range(len(S.keys())):

        elem = [matrix_sv[i][j]*x[j].solution_value for j,var_e in x_keys.items()]
        min_ = min([max(elem)-t[i],0])
        z += [min_]

    return np.array(z)

      
def job_affinity(t,z):
    
    sum = 0
    den = 0
    for i in range(0,len(t)):
        try:
            sum += np.abs(t[i] + z[i].solution_value)
        except AttributeError:
            sum += np.abs(t[i] + z[i])
        den += np.abs(t[i])
        
    return (sum/den)*100

        

        
def writing_job_affinity(job_affinity):
    
    jobs_id = list(job_affinity.keys())
    affinity = []
    for j in jobs_id:
        affinity.append(job_affinity[j])
    
    with open('job_affinity.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(jobs_id)
        spamwriter.writerow(affinity)

    return None  
                
        

if __name__ == '__main__':
    
    path = os.getcwd()
    foulder = os.path.join(path,'data')
    file1 = os.path.join(foulder,"courses.json")
    file2 = os.path.join(foulder,"jobs.json")
    file3 = os.path.join(foulder,"sfia.json")
    file4 = os.path.join(foulder,"units.json")
    
    files = [file1,file2,file3,file4]
    
    parser = ap.ArgumentParser()
    parser.add_argument('-n', type=int, default=6, help='n')
    parser.add_argument('-p', type=float, default=1, help='p')
    parser.add_argument('-c', type=int, default=240, help='c')
    parser.add_argument('-l', type=int, default=7, help='l: maximum level. Default: 7')
    parser.add_argument('-b', type=float, default=0.0, help='percentage of bachelor completed')
    parser.add_argument('-j', type=str, default='0', help='Job index')
    parser.add_argument('-s', type=str, default='au', help='Start semester')
    parser.add_argument('-i', type=int, default=None, help='Student ID')
    parser.add_argument('-y', help='compute job affinity for students', action='store_true')
    parser.add_argument('-m', help='computes the sum of skill levels', action='store_true' )
    parser.add_argument('-t', help='compute all the jobs', action='store_true')
    parser.add_argument('-z', help='compute job affinity for students', action='store_true')
    parser.add_argument('--cp', help='complex cp', action='store_true')
    parser.add_argument('-g', type=str, default = 'none', help='store results in csv')
    parser.add_argument('-f', type=str, default = 'none', help='store results in csv')
    args = parser.parse_args()
    
    if args.p == -1:
        p = 'inf'
    else:
        p = args.p
    
    job_id = args.j
    c_T = args.c
    n_sem = args.n
    fs = args.s
    s_id = args.i
    b = args.b
    m_lev = args.l

    course,U,S,J = data_dict(files)
    seasons = ["au","sp"]
    
    print(f"n \t | job \t | ja cp (%) | ja ap (%) | time cp (s) | time ap (s)")
    print(f"----------------------------------------------------------")
    counter_ = 1
    for job_id,job in J.items():
        matrices = array_creation(course,U,S,J,job_id,seasons,n_sem,f_sem=fs,m_cred=40,max_level=m_lev)   
        L,x_keys,B,P,C,D,d,R,or_,r,E,F,f,G,g,t,A,K,keys = matrices

        model,variables,constraint_keys,model_time,matrix_sv = model_cp(matrices,c_T,S)
        x,v = variables
        assignments,f_,solve_time_cp = solve_model(model,x,x_keys,True)
        z = z_vec(x,x_keys,S,matrix_sv)
        alpha_cp = job_affinity(t,z)
        
        model,variables,constraint_keys,model_time = model_cplex(matrices,c_T)
        x,v,y,z,zl = variables
        assignments,f_,solve_time_ap = solve_model(model,x,x_keys,False)
        alpha_ap = job_affinity(t,z)

        print(f"{counter_} \t | {job_id} \t | {alpha_cp:.2f} | {alpha_ap:.2f} | {solve_time_cp:.3f} | {solve_time_ap:.3f} ")
        counter_ += 1
        

    """
    
    matrices = array_creation(course,U,S,J,job_id,seasons,n_sem,f_sem=fs,m_cred=40,max_level=m_lev)   
    L,x_keys,B,P,C,D,d,R,or_,r,E,F,f,G,g,t,A,K,keys = matrices
    if args.cp:
        model,variables,constraint_keys,model_time,matrix_sv = model_cp(matrices,c_T,S)
        x,v = variables
    else:
        model,variables,constraint_keys,model_time = model_cplex(matrices,c_T)
        x,v,y,z,zl = variables


    assignments,f_,solve_time = solve_model(model,x,x_keys,args.cp)
    print_plan(assignments,L)
    print(f"Solving time = {solve_time:.2f}s")
    if args.cp:
        z = z_vec(x,x_keys,S,matrix_sv)
    alpha = job_affinity(t,z)
    print("------------------------------------")
    print(f"Job affinity = {alpha:.2f}%")

        
    """