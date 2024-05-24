Degree Planning
===================
This repository contains the implementation of the algorithms and data of the experimental section of the paper
"Computing Job-Tailored Degree Plans Towards the Acquisition of Professional Skills" by Roger X. Lera-Leri, Filippo Bistaffa, Tomas Trescak, and Juan A. Rodríguez-Aguilar, 2024.

Dependencies
----------
 - [Python 3](https://www.python.org/downloads/)
 - [docplex](https://ibmdecisionoptimization.github.io/docplex-doc/)
 - [Numpy](https://numpy.org/)
 - [CPLEX 22.1.0](https://www.ibm.com/docs/en/icos)

Dataset
----------
All experiments consider the [Bachelor Degree](https://hbook.westernsydney.edu.au/programs/bachelor-information-communications-technology/) of Information and Communications Technology from the [Western Sydney University](https://www.westernsydney.edu.au/).

Execution
----------
Our approach must be executed by means of the [`problem.py`](problem.py) Python script, i.e.,
```
usage: problem.py [-h] [-p P] [-n N] [-c C] [-l L] [-j J] [-s S] [--docplex]

optional arguments:
  -h, --help  show this help message and exit
  -p P        p-norm (default: 1)
  -n N        number of semesters (default: 6)
  -c C        number of credits to complete (default: 240)
  -l L        maximum skill level (default: 7)
  -j J        job index (default: '0')
  -s S        Start semester: ['au','sp'] (default: 'au')
  --docplex   computes the solution for the docplex transformation
```
