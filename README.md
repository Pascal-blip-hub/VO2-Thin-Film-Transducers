# VO2-Thin-Film-Transducers

## Overview
In a recent paper (in submission) we show how VO2 thin-film transducers can be utilized to determine the thermal conductivity of various bulk materials. This repository provides the Python code to perform thermal analysis with an analytical model as well as a COMSOL model.

## Context
During steady-state laser irradiation of a bulk sample's surface coated with a thin-film VO2 layer, a first-order phase transition from an insulating to a metallic phase will occur if the temperature exceeds 341 K. Both phases differ greatly with respect to their optical properties. The spot size of the metallic phase not only relies on the input power of the irradiating laser and the average VO2 thermal conductivity, but also on the sample's thermal conductivity. In the paper, an analytical model is described, linking the resulting metallic spot size to its respective laser input power. To obtain the curves NORMALIZED RADIUS(NORMALIZED POWER) and MINIMUM POWER(THERMAL CONDUCTIVITY RATIO) from the analytical model, a numerical integration is necessary. Further, the first curve is reproduced with a finite element method in COMSOL Multiphysics. This repository contains the code to reproduce the Radius vs. Power curves, both analytically and numerically, as well as the Minimum Power vs. Thermal Conductivity Ratio curve in an analytical manner. The code is designed to automate simulations while maintaining flexibility for embedding into your own programs. 

## Repository Structure
In total, four Python scripts and two COMSOL model files are provided. The utils.py file solely contains utility functions that are used in the main scripts. The files RAD_POW_ANA.py and RAD_POW_FEM.py are for generating Radius vs. Power curves analytically and numerically, respectively. The MINPOW_RHO_ANA.py file is for generating the Minimum Power vs. Thermal Conductivity Ratio curve. The provided COMSOL model files contain the geometry, material selection and a precomputed meshing. Note that the meshing might be refined, depending on your calculations. Note that the Example_File_Interfacial_Resistance.mph is only needed if you want to incorporate the effect of interfacial thermal resistance between the sample and the VO2 coating. 

## Requirements
Apart from standard libraries like numpy, os and scipy, an installation of COMSOL Multiphysics (ideally version 6.2) in combination with the mph library is necessary to run the COMSOL simulations.

## Authors
Pascal J. Schroeder  
Sorbonne Université, CNRS, Institut des NanoSciences de Paris, 75005 Paris, France  
RWTH Aachen University, 52056 Aachen, Germany

## Contact
pascal.schroeder@rwth-aachen.de  
james.utterback@sorbonne-universite.fr  
jose.ordonez@cnrs.fr



