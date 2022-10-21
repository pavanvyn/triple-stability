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
        mlp_stable = mlp_predict[0,1] < 0.5

    return mlp_stable


# inputs qi, q0, al, ei, eo, im ALL should be either floating point intergers or 1D numpy arays of the SAME lengths
def form_classifier(qi, qo, al, ei, eo, im):
    LK_ei_sq = 1 - (5./3.)*np.cos(im)**2
    ei = np.where( LK_ei_sq >= 0, np.maximum( ei, 0.5*LK_ei_sq ), ei )
    fac = 0.125*(1.0 - 0.2*ei + eo) * (np.cos(im) - 1.0) + 1.0

    Y = (1.0 - eo) / ((1.0 + ei) * al)
    Y_crit = 2.4 * pow( (1.0 + qo),2.0/5.0 ) * pow( (1.0 + ei),-2.0/5.0 ) * pow( (1.0 - eo),-1.0/5.0 ) * fac
    if (Y < Y_crit):
        form_stable = False
    else:
        form_stable = True

    return form_stable


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-qi","--mratio_inner",help="inner mass ratio m2/m1 < 1, m2<m1", default=1.0, type=float)
    parser.add_argument("-qo","--mratio_outer",help="outer mass ratio m3/(m1+m2)", default=0.5, type=float)
    parser.add_argument("-al","--aratio",help="semimajor axis ratio a_in/a_out < 1", default=0.2, type=float)
    parser.add_argument("-ei","--ecc_inner",help="inner eccentricity", default=0.0, type=float)
    parser.add_argument("-eo","--ecc_outer",help="outer eccentricity", default=0.0, type=float)
    parser.add_argument("-im","--inc_mutual",help="mutual inclination, in radian", default=0.0, type=float)
    args = parser.parse_args()

    mlp_pfile = "./mlp_model_trip.pkl"

    print("Inner mass ratio:",args.mratio_inner)
    print("Outer mass ratio:",args.mratio_outer)
    print("Semimajor axis ratio:",args.aratio)
    print("Inner eccentricity:",args.ecc_inner)
    print("Outer eccentricity:",args.ecc_outer)
    print("Mutual inclination:",args.inc_mutual)
    print()

    mlp_stable = mlp_classifier(mlp_pfile, args.mratio_inner, args.mratio_outer, args.aratio, args.ecc_inner, args.ecc_outer, args.inc_mutual)
    mlp_stable_string = "ML stable" if mlp_stable else "ML unstable"

    form_stable = form_classifier(args.mratio_inner, args.mratio_outer, args.aratio, args.ecc_inner, args.ecc_outer, args.inc_mutual)
    form_stable_string = "Formula stable" if mlp_stable else "Formula unstable"

    print(mlp_stable_string)
    print(form_stable_string)
