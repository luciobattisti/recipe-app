#!/usr/bin/env bash

source /opt/miniconda3/etc/profile.d/conda.sh
conda activate recipe-env
cd $HOME/Applications/recipe-app
python RecipeApp.py

