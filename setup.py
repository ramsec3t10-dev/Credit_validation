from setuptools import setup,find_packages
import os,sys
from typing import List

from Credit_validation.exception.exception import   CreditDataException

def get_requirements()->List[str]:
    try:
        requirements_lst:List[str] = []
        with open("requirements.txt","r")as file:
            lines = file.readline()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirements_lst.append(requirement)
    except FileNotFoundError as e:
        print("Requirements.txt file not found")
    return requirements_lst

print(get_requirements())  

setup(  #setting up meta data
      name = "Credit_Validation",
      version = "0.0.1",
      author = "Saint Ram",
      author_email = "rams.ec3t10@gct.ac.in",
      packages = find_packages(),
      install_requires = get_requirements()
)
