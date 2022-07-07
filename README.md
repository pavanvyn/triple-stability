Code to check if a given configuration of a triple-star system is dynamically stable

The first step is to install the scikit-learn package (if not already available) using the following terminal command:

    pip3 install scikit-learn
    
After changing to the repository directory, the python3 module is run on the terminal as follows:

    python3 mlp_classify.py -qi 1.0 -qo 0.5 -al 0.2 -ei 0.0 -eo 0.0 -im 0.0
    
Here, the arguments qi, qo, al, ei, eo and im refer to  $$q_{\mathrm{in}} = m_2 / m_1 \leq 1$$ ,  $q_{\mathrm{out}} = m3 / (m1+m2)$ , $\alpha = a_{\mathrm{in}} / a_{\mathrm{out}} \leq 1$ ,  $e_{\mathrm{in}} $ ,  $e_{\mathrm{out}}$  and  $i_{\mathrm{mut}}$  respectively.

It is also possible to import the MLP classifier to another custom python3 script. The input parameters can also be numpy arrays, as shown in the sample script below:

    import numpy as np
    from mlp_classify import mlp_classifier

    # generate initial numpy arrays qi, qo, al, ei, eo, im

    mlp_pfile = "./mlp_model_best.pkl"

    mlp_stable = mlp_classifier(mlp_pfile, qi, qo, al, ei, eo, im)

    # returns True if stable, False if unstable
