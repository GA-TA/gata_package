from setuptools import setup

setup(
    name='GA-TA',
    version='1.0',
    description='GA-TA program is used to convert an easy-to-build generic table \
			    into more complex tables in the specific format required to use with Structure,\
			    Arlequin, and R softwares. GA-TA is applicable to autosomic, mitochondrial and \
			    X chromosome data. The program is written in Python under an open source policy, \
			    allowing experienced users to download the program from the github repository \
			    (https://github.com/santimda/GA-TA) and adapt it by adding new modules upon convenience.',
    license='GPLv3',
    packages=['gata'],
    author='del Palacio, S.; Di Santo, P.; Gamboa Lerena, M. M., Lopez Armengol, F. G.',
    author_email='martingamboa2@gmail.com',
    keywords=['Structure','Arlequin','R'],
    url='gata.fcaglp.unlp.edu.ar'
)