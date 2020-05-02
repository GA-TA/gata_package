# GA-TA 

## Introduction
**GA-TA**  program is used to convert an easy-to-build generic table into more complex tables in the specific format required to use with Structure, Arlequin, and R softwares. GA-TA is applicable to autosomic, mitochondrial and X chromosome data. The program is written in Python under an open source policy, allowing experienced users to download the program from the github repository (https://github.com/santimda/GA-TA) and adapt it by adding new modules upon convenience.

## Running online
 A stable version of the program can be executed on a friendly user environment on this [GA-TA website](http://gata.fcaglp.unlp.edu.ar/).

## Running on terminal

**GA-TA** is a Python module. You can install in your local environment doing:
   
   >$ python setup.py install

and you can enjoy GA-TA as Python3 module. You have a pipeline called main.py as an example of how to wrok with it.

To execute the example from the command line, run:
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

All columns with information must have a name (e.g., there cannot be a blank cell in the first row for any column with information). An example sheet along with a more detailed manual can be downloaded from the [GA-TA website](http://gata.fcaglp.unlp.edu.ar/), and they are also available in the folder 'Documentation'.
