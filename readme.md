# HARA-TOOL

## Executive summary

This is an attempt to create a tool for automated Hazard Analysis and Risk Assessment as per ISO 26262.

## Description

### Inputs

* System functions
* List of keywords for HazOp
* List of road situatuions

### Outputs

* Risk parameters:
  * *S* -- serverity
  * *E* -- exposure
  * *C* -- controllability
  * *ASIL* -- automotive safety integrity level
* Formulation of a safety goal.

## Scripts
### ```hazop.py```
Usage: python hazop.py <functions_file> <keywords_file>
Returns malfunctions
