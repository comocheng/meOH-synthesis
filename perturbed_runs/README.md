## Parametric Uncertainty
The basic idea is to perturb some thermo and kinetic parameters and then run RMG ~5000 times to see which combination of parameters will match the experimental results (closeness is based on matching the concnetration over temperature profiles for a few key species. Bjarne used mean-absolute percent error

DOI: 10.1021/jacsau.1c00276 	


## Steps to reproduce

1. Coarse runs - run RMG enough times that you are confident in the graph of the mechanism. This allows you to put additional constraints into the input.py along with all of the pre-filled species that will end up in the mechanism. The goal is to be able to run RMG really fast so you can run it lots of times.

2. Fine runs - perturb the thermo and kinetic parameters and run RMG a ton of times
- Copy a version of RMG-database to hold all the thousands of copies of library files
- Run the parameter perturbation script


