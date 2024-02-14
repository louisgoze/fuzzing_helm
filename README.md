# Helm fuzzer - preliminary version

The scope of this repo is to show you how to get started with the project. Feel free to take inspiration from this and further develop it. 

## Prerequisites
You need to install the different security linters for Kubernetes. Currently they are:
- [checkov](https://github.com/bridgecrewio/checkov)

## Install

This app requires [pipenv](https://pipenv.pypa.io/en/latest/) to be available and installed. 

Run `pipenv install` to automatically download all the needed dependencies

## Run 

A simple way to run the script is: 

`pipenv run python main.py -f input/example.yml`


TODOs

- Expand the number of security checkers (currently there is only checkov)
- Expand the fuzzing rules 
- How to handle multiple outputs for the same input?
