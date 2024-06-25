import pickle
import numpy as np


# inputs qi, q0, al, ei, eo, im ALL should be either floating point intergers or 1D numpy arays of the SAME lengths
def mlp_classifier(mlp_pfile, qi, qo, al, ei, eo, im):
    with open(mlp_pfile,'rb') as pfile:
        mlp = pickle.load(pfile) # load model from file

    mlp_predict = mlp.predict_proba( np.c_[qi, qo, al, ei, eo, im/np.pi] ) # inclination normalised to 0-1
    if mlp_predict.shape[0] == 1:
        mlp_stable = mlp_predict[0,1] < 0.5
    else:
        mlp_stable = mlp_predict[:,1] < 0.5

    return mlp_stable


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-qi","--mratio_inner",help="inner mass ratio m2/m1 <= 1, m2<=m1", default=1.0, type=float)
    parser.add_argument("-qo","--mratio_outer",help="outer mass ratio m3/(m1+m2)", default=0.5, type=float)
    parser.add_argument("-al","--aratio",help="semimajor axis ratio a_in/a_out < 1", default=0.2, type=float)
    parser.add_argument("-ei","--ecc_inner",help="inner eccentricity", default=0.0, type=float)
    parser.add_argument("-eo","--ecc_outer",help="outer eccentricity", default=0.0, type=float)
    parser.add_argument("-im","--inc_mutual",help="mutual inclination, in radian", default=0.0, type=float)
    args = parser.parse_args()

    # mlp_pfile = "./mlp_model_trip_v1.2.2.pkl" # change in semimajor axes definition
    mlp_pfile = "./mlp_model_trip_ghost_v1.2.2.pkl" # divergence of similar ('ghost') orbits definition

    mlp_stable = mlp_classifier(mlp_pfile, args.mratio_inner, args.mratio_outer, args.aratio, args.ecc_inner, args.ecc_outer, args.inc_mutual)
    mlp_stable_string = "System is stable" if mlp_stable else "System is unstable"

    print(mlp_stable_string)
