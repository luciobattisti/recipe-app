#!/usr/bin/env bash

source $HOME/miniconda3/etc/profile.d/conda.sh
conda activate recipe-env
cd $HOME/Applications/recipe-app
python RecipeApp.py

