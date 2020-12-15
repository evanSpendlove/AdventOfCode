#!/bin/bash

# Ask user for the day number
read num
# Setup environment
source ./bin/activate
export AOC_SESSION=53616c7465645f5fe4892f663b4332fcac3ca013250fc931afff4db8ce49779127fa14280d8295f854f54cd4bb7d038c

# Make new folder for the day and fill with base files
mkdir day_$num
cd day_$num
aocd $num > input.in
touch day$num.py
