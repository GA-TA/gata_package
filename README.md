# GA-TA 

## Introduction
**GA-TA**  program converts an easy-to-build generic table into more complex tables in the specific format required by commonly-used softwares in genetics (namely _Structure_, _Arlequin_, and _R_ softwares). GA-TA is applicable to autosomic, X chrosome and Y chromosome data. The program is written entirely in Python3 under an open source policy, allowing experienced users to download the program from the github repository (https://github.com/GA-TA/gata_package) and adapt it by adding new modules upon convenience.

## Running online
 A stable version of the program can be executed on a friendly user environment on this [GA-TA website](http://gata.fcaglp.unlp.edu.ar/).

## Running on terminal

**GA-TA** is a Python3 module. You can install it in your local environment by downloading the github repository and running in a terminal:
   
   >$ python setup.py install

From now on you can enjoy GA-TA as a Python module. 

You have a pipeline called _main.py_ as an example of how to work with it. To execute the example from the command line, run:
   >$ python main.py [OPTIONS] <spreadsheet_name>  

## Installation with conda environment for Python 3.X:
.. Install miniconda
.. Create myenv
$  conda create -n myenv python=3.X
.. Activate environment
$  conda activate myenv
.. Install the following packages using 'conda install pack':
. pandas
. xlrd
. unidecode
. openpyxl

[OPTIONS]: The user can specify one, two or three letters (in any order) to obtain the desired output tables. These are: "r" for R, "a" for Arlequin, and "s" for Structure. 

The spradsheet must be either in Excel extention '.xlsx' or in open office '.ods'

Examples:

	>$ python main.py ra spreadsheet.xlsx

will return output files for R and Arlequin.

	>$ python main.py s spreadsheet.xlsx

will return output files for Structure.

## Considerations 

All columns with information must have a name (e.g., there cannot be a blank cell in the first row for any column with information). An example sheet along with a more detailed manual are available in the folder 'Documentation' (these can also be downloaded from the [GA-TA website](http://gata.fcaglp.unlp.edu.ar/)).
