#! /usr/bin/env bash

# setup Python 2.7 and ROOT 6

#source /cvmfs/sft.cern.ch/lcg/external/gcc/4.9.1/x86_64-slc6-gcc48-opt/setup.sh
source /cvmfs/sft.cern.ch/lcg/contrib/gcc/4.9/x86_64-slc6/setup.sh
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.06.08/x86_64-slc6-gcc49-opt/root/bin/thisroot.sh

#/sft.cern.ch/lcg/views/ROOT-latest/x86_64-slc6-gcc49-opt/setup.sh
source /opt/rh/python27/enable


#which root
 # unset PYTHONPATH
 # export PYTHONPATH=:/lib
 # unset PYTHONHOME

# Install virtualenvwrapper package if not already installed
if [ ! -f ~/.local/bin/virtualenvwrapper.sh ]; then
  # deleting cached packages to force download
  rm -rf ~/.cache/pip/
  pip install --user -I virtualenvwrapper
fi

# Create virtual env and install dependencies
if [ ! -d ~/.virtualenvs/hgc_tpg/ ]; then
  mkdir -p ~/.virtualenvs/
  export WORKON_HOME=~/.virtualenvs
  export VIRTUALENVWRAPPER_PYTHON=`which python`
  export VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv
  source ~/.local/bin/virtualenvwrapper.sh
  mkvirtualenv hgc_tpg
  # deleting cached packages to force download
  rm -rf ~/.cache/pip/
  pip install -r requirements.txt -I
  pip install -e .
else
  export WORKON_HOME=~/.virtualenvs
  export VIRTUALENVWRAPPER_PYTHON=`which python`
  export VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv
  source ~/.local/bin/virtualenvwrapper.sh
  workon hgc_tpg
  # Check if all the package requirements are satisfied
  available_dep_count=$(pip freeze | grep -f requirements.txt | wc -l)
  needed_dep_count=$(cat requirements.txt | wc -l)
  if [ "$available_dep_count" != "$needed_dep_count" ]; then
    echo "Updating dependencies"
    # deleting cached packages to force download
    rm -rf ~/.cache/pip/
    pip install -r requirements.txt -I
  fi
fi
