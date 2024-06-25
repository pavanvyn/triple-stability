import pickle
import numpy as np


# inputs qi, q0, al, ei, eo, im ALL should be either floating point intergers or 1D numpy arays of the SAME lengths
def mlp_classifier_3p1(mlp_pfile, qi, qm, qo, alim, almo, ei, em, eo, iim, iio, imo):
    with open(mlp_pfile,'rb') as pfile:
        mlp = pickle.load(pfile) # load model from file

    mlp_predict = mlp.predict_proba( np.c_[qi, qm, qo, alim, almo, ei, em, eo, iim/np.pi, iio/np.pi, imo/np.pi] ) # inclination normalised to 0-1
    if mlp_predict.shape[0] == 1:
        mlp_stable = mlp_predict[0,1] < 0.5
    else:
        mlp_stable = mlp_predict[:,1] < 0.5

    return mlp_stable


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-qi","--mratio_inner",help="inner mass ratio m2/m1 <= 1, m2<=m1", default=1.0, type=float)
    parser.add_argument("-qm","--mratio_intermediate",help="intermediate mass ratio m3/(m1+m2) (best if < ~ 3)", default=0.5, type=float)
    parser.add_argument("-qo","--mratio_outer",help="outer mass ratio m4/(m1+m2+m3) (best if < ~ 2)", default=0.33, type=float)
    parser.add_argument("-alim","--aratio_inner_intermediate",help="semimajor axis ratio a_in/a_mid < 1", default=0.2, type=float)
    parser.add_argument("-almo","--aratio_intermediate_outer",help="semimajor axis ratio a_mid/a_out < 1", default=0.2, type=float)
    parser.add_argument("-ei","--ecc_inner",help="inner eccentricity", default=0.0, type=float)
    parser.add_argument("-em","--ecc_intermediate",help="intermediate eccentricity", default=0.0, type=float)
    parser.add_argument("-eo","--ecc_outer",help="outer eccentricity", default=0.0, type=float)
    parser.add_argument("-iim","--inc_inner_intermediate",help="mutual inclination of inner-intermediate, in radian", default=0.0, type=float)
    parser.add_argument("-iio","--inc_inner_outer",help="mutual inclination of inner-outer,  in radian", default=0.0, type=float)
    parser.add_argument("-imo","--inc_intermediate_outer",help="mutual inclination of intermediate-outer, in radian", default=0.0, type=float)
    args = parser.parse_args()

    mlp_pfile = "./mlp_model_3p1_ghost_v1.2.2.pkl"

    mlp_stable = mlp_classifier_3p1(mlp_pfile, args.mratio_inner, args.mratio_intermediate, args.mratio_outer, args.aratio_inner_intermediate, args.aratio_intermediate_outer, \
                                    args.ecc_inner, args.ecc_intermediate, args.ecc_outer, args.inc_inner_intermediate, args.inc_inner_outer, args.inc_intermediate_outer)
    mlp_stable_string = "System is stable" if mlp_stable else "System is unstable"

    print(mlp_stable_string)
