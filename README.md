# VO2-Thin-Film-Transducers

## Overview
In a recent paper (in submission) we show how VO2 thin-film transducers can be utilized to determine the thermal conductivity of various bulk materials. This repository provides the code to perform automated thermal analysis with an analytical as well as a finite element method (FEM) model.

## Context
During steady-state laser irradiation of a bulk sample's surface coated with a thin-film VO2 layer, a first-order phase transition from an insulating to a metallic phase will occur if the temperature exceeds 341 K. Both phases differ greatly with respect to their optical properties. The spot size of the metallic phase does not only rely on the input power of the irradiating laser and the average VO2 thermal conductivity, but also on the sample's thermal conductivty. In the paper, an analytical model is described, linking the resulting metallic spot size to its respective laser input power. To obtain the curves NORMALIZED RADIUS(NORMALIZED POWER) and MINIMUM POWER(THEHRMAL CONDUCTIVITY RATIO) from the analytical model, a numerical integration. Further, the first curve is reproduced with a finite element method in COMSOL Multiphysics. This repository contains the code to reproduce the Radius vs. Power curves, both analytically and numerically, as well as the Minimum Power vs. Thermal Conductivity Ratio curve in an analytical manner. The code is designed to automate simulations while maintaining flexibility for embeddement into own programs. 

## Repository Structure




