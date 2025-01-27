# Stability classification of triple-star systems

This repository contains a simple `python3` (3.10.0 or higher) code to check if a given configuration of a triple-star system is dynamically stable. Please refer to Vynatheya et al. (2022) (see https://ui.adsabs.harvard.edu/abs/2022MNRAS.516.4146V/abstract) and Vynatheya et al. (2023) (see https://ui.adsabs.harvard.edu/abs/2023arXiv230109930V/abstract) for details regarding the multi-layer perceptron classifier. A `C`/`C++` interface is also provided.

Two MLP models are provided, using different defining criteria for stability. In Vynatheya et al. (2022), stabililty is defined on the basis of change in semimajor axes. Alternatively, in Vynatheya et al. (2023), stability is defined on the basis of divergence of similar ('ghost') orbits. Refer to both papers for details, if required.

The first step is to install a compatible version (1.0.2 or 1.2.2) of the scikit-learn package (the latest version should also work, but throws a warning of potential incompatibility) using the following terminal command:

    # pip3 install -v scikit-learn==1.0.2
    pip3 install -v scikit-learn==1.2.2


## Implementing our classifiers in `python3` (simplest option)

After changing to the repository directory, the python3 module is run on the terminal as follows:

    python3 classify_trip.py -qi 1.0 -qo 0.5 -al 0.2 -ei 0.0 -eo 0.0 -im 0.0
    
Here, the arguments are:

1) `qi` (inner mass ratio):   $10^{-2} \leq q_{\mathrm{in}} = m_2 / m_1 \leq 1$
2) `qo` (outer mass ratio):   $10^{-2} \leq q_{\mathrm{out}} = m_3 / (m_1+m_2) \leq 10^{2}$
3) `al` (semimajor axis ratio):   $10^{-4} \leq \alpha = a_{\mathrm{in}} / a_{\mathrm{out}} \leq 1$
4) `ei` (inner eccentricity):   $0 \leq e_{\mathrm{in}} \leq 1$
5) `eo` (outer eccentricity):   $0 \leq e_{\mathrm{out}} \leq 1$
6) `im` (mutual inclination):   $0 \leq i_{\mathrm{mut}} \leq \pi$

It is also possible to import the MLP classifier to another custom python3 script. The input parameters can also be numpy arrays, as shown in the sample script below:

    import numpy as np
    # 'import sklearn' is not necessary, but scikit-learn needs to be installed
    from classify_trip import mlp_classifier

    # generate initial numpy arrays qi, qo, al, ei, eo, im

    # mlp_pfile = "./mlp_model_trip_v1.2.2.pkl" # change in semimajor axes definition
    mlp_pfile = "./mlp_model_trip_ghost_v1.2.2.pkl" # divergence of similar ('ghost') orbits definition

    mlp_stable = mlp_classifier(mlp_pfile, qi, qo, al, ei, eo, im)
    
    # mlp_stable stores True if stable, False if unstable


## Implementing our classifiers in `C`/`C++`

One way to include our classifiers in `C` is to use a `python` interface. This is done by including the `Python.h` header file. This should already be present in your system by default, but if not, python3-dev should be installed. `classify_trip_wrapper.c` implements this and should be compiled as folllows:

    gcc classify_trip_wrapper.c -o classify_trip_wrapper.out -I /usr/include/python3.10 -lpython3.10

The `-I` flag is only necessary if the `python` header files are not in the system path, and the `-lpython3.10` flag allows `C` to interact with `python3` (3.10.0 or higher). To include the wrapper script in a custom `C`/`C++` script, it is sufficient to include the header file `classify_trip_wrapper.h`. In this case, comment out/remove the `main()` function from `classify_trip_wrapper.c`. An example is as follows:

    #include "classify_trip_wrapper.h"

    int main() {
        // char mlp_pfile[] = "./mlp_model_trip_v1.2.2.pkl"; // change in semimajor axes definition
        char mlp_pfile[] = "./mlp_model_trip_ghost_v1.2.2.pkl"; // divergence of similar ('ghost') orbits definition

        double qi, qo, al, ei, eo, im;
        
        // define these quantities

        int mlp_stable = mlp_classifier(mlp_pfile, qi, qo, al, ei, eo, im);

        // mlp_stable stores 1 if stable, 0 if unstable

        return 0;
    }

This custom script (`C` and `C++` respectively) is compiled similarly:

    gcc my_program.c classify_trip_wrapper.c -o my_program.out -I /usr/include/python3.10 -lpython3.10
    g++ my_program.cpp classify_trip_wrapper.c -o my_program.out -I /usr/include/python3.10 -lpython3.10


## Citing our work

If these classification models are used for research, please cite our papers - https://ui.adsabs.harvard.edu/abs/2022MNRAS.516.4146V/abstract (mlp_model_trip.pkl) or https://ui.adsabs.harvard.edu/abs/2023arXiv230109930V/abstract (mlp_model_trip_ghost.pkl).

Enjoy classifying!
