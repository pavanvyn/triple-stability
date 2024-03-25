#include "classify_trip_wrapper.h"
#include <stdio.h>
#include <Python.h>

int mlp_classifier(char *mlp_pfile, double qi, double qo, double al, double ei, double eo, double im) {
    // initialize Python interpreter
    Py_Initialize();

    // append current directory to Python's module search path
    PyObject *sys_module = PyImport_ImportModule("sys");
    PyObject *sys_path = PyObject_GetAttrString(sys_module, "path");
    PyObject *current_dir = PyUnicode_FromString(".");
    PyList_Append(sys_path, current_dir);

    // import Python module
    PyObject *py_classify_trip_module = PyImport_ImportModule("classify_trip");
    if (py_classify_trip_module == NULL) {
        PyErr_Print();
        Py_Finalize();
        return -1;
    }

    // get reference to Python function
    PyObject *py_mlp_classifier_func = PyObject_GetAttrString(py_classify_trip_module, "mlp_classifier");
    if (py_mlp_classifier_func == NULL) {
        PyErr_Print();
        Py_DECREF(py_classify_trip_module);
        Py_Finalize();
        return -1;
    }

    // prepare Python function arguments    
    PyObject *py_mlp_classifier_args = Py_BuildValue("(sdddddd)", mlp_pfile, qi, qo, al, ei, eo, im);
    if (py_mlp_classifier_args == NULL) {
        PyErr_Print();
        Py_DECREF(py_classify_trip_module);
        Py_DECREF(py_mlp_classifier_func);
        Py_Finalize();
        return -1;
    }

    // call Python function 
    PyObject *py_mlp_stable_ret = PyObject_CallObject(py_mlp_classifier_func, py_mlp_classifier_args);
    if (py_mlp_stable_ret == NULL) {
        PyErr_Print();
        Py_DECREF(py_classify_trip_module);
        Py_DECREF(py_mlp_classifier_func);
        Py_DECREF(py_mlp_classifier_args);
        Py_Finalize();
        return -1;
    }
    
    // convert return value to C boolean
    int mlp_stable = PyObject_IsTrue(py_mlp_stable_ret);

    // clean up Python objects
    Py_DECREF(py_classify_trip_module);
    Py_DECREF(py_mlp_classifier_func);
    Py_DECREF(py_mlp_classifier_args);
    Py_DECREF(py_mlp_stable_ret);

    // finalize Python interpreter
    Py_Finalize();

    return mlp_stable;
}

int main() {
    // char mlp_pfile[] = "./mlp_model_trip_v1.2.2.pkl"; // change in semimajor axes definition
    char mlp_pfile[] = "./mlp_model_trip_ghost_v1.2.2.pkl"; // divergence of similar ('ghost') orbits definition

    double mratio_inner, mratio_outer, aratio, ecc_inner, ecc_outer, inc_mutual;
    mratio_inner = 1.0;
    mratio_outer = 0.5;
    aratio = 0.2;
    ecc_inner = 0.0;
    ecc_outer = 0.0;
    inc_mutual = 0.0;

    int mlp_stable = mlp_classifier(mlp_pfile, mratio_inner, mratio_outer, aratio, ecc_inner, ecc_outer, inc_mutual);
    
    const char *mlp_stable_string;
    if (mlp_stable == 1) mlp_stable_string = "ML stable"; 
    else if (mlp_stable == 0) mlp_stable_string = "ML unstable";
    else mlp_stable_string = "ERROR";
    printf("%s\n", mlp_stable_string);

    return 0;
}

// gcc classify_trip_wrapper.c -o classify_trip_wrapper.out -I /usr/include/python3.10 -lpython3.10
