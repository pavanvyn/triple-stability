import pickle
import numpy as np


# inputs qi, q0, al, ei, eo, im ALL should be either floating point intergers or 1D numpy arays of the SAME lengths
def mlp_classifier_2p2(mlp_pfile, qi1, qi2, qo, ali1o, ali2o, ei1, ei2, eo, ii1i2, ii1o, ii2o):
    with open(mlp_pfile,'rb') as pfile:
        mlp = pickle.load(pfile) # load model from file

    mlp_predict = mlp.predict_proba( np.c_[qi1, qi2, qo, ali1o, ali2o, ei1, ei2, eo, ii1i2/np.pi, ii1o/np.pi, ii2o/np.pi] ) # inclination normalised to 0-1
    if mlp_predict.shape[0] == 1:
        mlp_stable = mlp_predict[0,1] < 0.5
    else:
        mlp_stable = mlp_predict[:,1] < 0.5

    return mlp_stable


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-qi1","--mratio_inner1",help="inner1 mass ratio m2/m1 <= 1, m2<=m1", default=1.0, type=float)
    parser.add_argument("-qi2","--mratio_inner2",help="inner2 mass ratio m3/m4 <= 1, m4<=m3", default=1.0, type=float)
    parser.add_argument("-qo","--mratio_outer",help="outer mass ratio (m3+m4)/(m1+m2) <= 1, (m3+m4) <= (m1+m2)", default=1.0, type=float)
    parser.add_argument("-ali1o","--aratio_inner1_outer",help="semimajor axis ratio a_in1/a_out < 1", default=0.2, type=float)
    parser.add_argument("-ali2o","--aratio_inner2_outer",help="semimajor axis ratio a_in2/a_out < 1", default=0.2, type=float)
    parser.add_argument("-ei1","--ecc_inner1",help="inner1 eccentricity", default=0.0, type=float)
    parser.add_argument("-ei2","--ecc_inner2",help="inner2 eccentricity", default=0.0, type=float)
    parser.add_argument("-eo","--ecc_outer",help="outer eccentricity", default=0.0, type=float)
    parser.add_argument("-ii1i2","--inc_inner1_inner2",help="mutual inclination of inner1-inner2, in radian", default=0.0, type=float)
    parser.add_argument("-ii1o","--inc_inner1_outer",help="mutual inclination of inner1-outer,  in radian", default=0.0, type=float)
    parser.add_argument("-ii2o","--inc_inner2_outer",help="mutual inclination of inner2-outer, in radian", default=0.0, type=float)
    args = parser.parse_args()

    mlp_pfile = "./mlp_model_2p2_ghost_v1.2.2.pkl"

    mlp_stable = mlp_classifier_2p2(mlp_pfile, args.mratio_inner1, args.mratio_inner2, args.mratio_outer, args.aratio_inner1_outer, args.aratio_inner2_outer, \
                                    args.ecc_inner1, args.ecc_inner2, args.ecc_outer, args.inc_inner1_inner2, args.inc_inner1_outer, args.inc_inner2_outer)
    mlp_stable_string = "System is stable" if mlp_stable else "System is unstable"

    print(mlp_stable_string)
