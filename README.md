![Linux](https://img.shields.io/badge/-Linux-grey?logo=linux)
![Python](https://img.shields.io/badge/Python-v3.7%5E-orange?logo=python)

## Index

* [Description](#description)
* [Features](#features)
* [Installation](#installation)

## Description

**[worker-drunken-gait] The program creates an array of movements of positions of a given number of workers and builds a
 graph. 


## Features

* Automatic fill the needed initial variables.
* Separate configuration file.
* The number of workers (_NUMBER_OF_WORKERS_), the number of dimensions (_NUMBER_OF_DIMENSIONS_) has no limitations 
* Has the ability to set different values of motion probabilities.
* Has the ability to set different values for movement shifts - **STEP_SIZE**.
* The plotting function is only available for a **2-D** task.

## Installation

### 1. Create Virtual Python Environment and Install Python3 interpreter
Additional information on https://www.python.org/downloads/
and 
[Creation of virtual environments](https://docs.python.org/3/library/venv.html)

or simple way to create subfolder venv (with python packages) inside the current directory:

    $ python -m venv venv

### 2. Clone this repository into your directory

    $ mkdir app && cd app
    
    
    $ git clone https://github.com/xyz-man/worker-drunken-gait.git

### 3. Install requirements


    $ pip install -r requirements.txt
    
### 4. Configuration

Edit the `settings.py` file and change needed values. 
      
### 5. Run

Inside the root project directory (`.app/`) activate local virtual environments:

    $ source venv/bin/activate
    
and run `main.py` file:

    $ python main.py
    


### 6. License

Program has been created under the **GNU GPLv3 license**
