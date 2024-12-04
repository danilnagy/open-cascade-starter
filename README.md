# open-cascade-starter

## Install conda

https://www.anaconda.com/download/success

## Conda commands

conda config --add channels conda-forge

conda create --name=pyoccenv python=3.10
conda activate pyoccenv
conda install -c conda-forge pythonocc-core=7.8.1
conda deactivate
conda env remove --name pyoccenv
conda env list
