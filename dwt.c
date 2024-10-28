#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <stdio.h>
#include <stdlib.h>
#include <Python.h> // Connect with Python API
#include <numpy/arrayobject.h> 
#include "nrutil.h"  // Ensure nrutil.h and nrutil.c are available

#define C0 0.4829629131445341
#define C1 0.8365163037378079
#define C2 0.2241438680420134
#define C3 -0.1294095225512604

// Forward declarations
void daub4(float a[], unsigned long n, int isign);
void wt_one(float a[], unsigned long n, int isign, void (*wtstep)(float[], unsigned long, int));

// daub4 implementation
void daub4(float a[], unsigned long n, int isign) {
    float *wksp;
    unsigned long nh, nh1, i, j;

    if (n < 4) return;

    wksp = vector(1, n);  // Allocate memory (1-based indexing)
    nh1 = (nh = n >> 1) + 1;  // nh = n / 2; nh1 = nh + 1

    if (isign >= 0) {  // Forward transform
        for (i = 1, j = 1; j <= n - 3; j += 2, i++) {
            wksp[i] = C0 * a[j] + C1 * a[j + 1] + C2 * a[j + 2] + C3 * a[j + 3];
            wksp[i + nh] = C3 * a[j] - C2 * a[j + 1] + C1 * a[j + 2] - C0 * a[j + 3];
        }
        wksp[i] = C0 * a[n - 1] + C1 * a[n] + C2 * a[1] + C3 * a[2];
        wksp[i + nh] = C3 * a[n - 1] - C2 * a[n] + C1 * a[1] - C0 * a[2];
    } else {  // Inverse transform
        wksp[1] = C2 * a[nh] + C1 * a[n] + C0 * a[1] + C3 * a[nh1];
        wksp[2] = C3 * a[nh] - C0 * a[n] + C1 * a[1] - C2 * a[nh1];
        for (i = 1, j = 3; i < nh; i++) {
            wksp[j++] = C2 * a[i] + C1 * a[i + nh] + C0 * a[i + 1] + C3 * a[i + nh1];
            wksp[j++] = C3 * a[i] - C0 * a[i + nh] + C1 * a[i + 1] - C2 * a[i + nh1];
        }
    }

    for (i = 1; i <= n; i++) a[i] = wksp[i];  // Copy back to original array
    free_vector(wksp, 1, n);  // Free allocated memory
}

// wt_one wrapper function
void wt_one(float a[], unsigned long n, int isign, void (*wtstep)(float[], unsigned long, int)) {
    unsigned long nn;

    if (n < 4) return;  // Not enough data to transform

    if (isign >= 0) {  // Forward transform
        for (nn = n; nn >= 4; nn >>= 1) {
            (*wtstep)(a, nn, isign);  // Call the step function
        }
    } else {  // Inverse transform
        for (nn = 4; nn <= n; nn <<= 1) {
            (*wtstep)(a, nn, isign);  // Call the step function
        }
    }
}

static PyObject *py_call_wt1(PyObject *self, PyObject *args) {
    PyObject *input_obj;
    int isign;

    if (!PyArg_ParseTuple(args, "Oi", &input_obj, &isign)) {
        return NULL;
    }

    PyArrayObject *data_in = (PyArrayObject *)PyArray_FROM_OTF(
        input_obj, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
    if (!data_in) {
        PyErr_SetString(PyExc_TypeError, "Failed to convert input to numpy array");
        return NULL;
    }

    int length = (int)PyArray_SIZE(data_in);

    float *float_data = (float *)malloc((length + 1) * sizeof(float));
    if (!float_data) {
        Py_DECREF(data_in);
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        return NULL;
    }

    double *data_ptr = (double *)PyArray_DATA(data_in);
    for (int i = 0; i < length; i++) {
        float_data[i + 1] = (float)data_ptr[i];
    }

    wt_one(float_data, length, isign, daub4); // Forward transform

    npy_intp dims[1] = {length};  // shape of output array
    PyObject *result = PyArray_SimpleNew(1, dims, NPY_DOUBLE);
    if (!result) {
        free(float_data);
        Py_DECREF(data_in);
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate result numpy array");
        return NULL;
    }

    double *result_ptr = (double *)PyArray_DATA((PyArrayObject *)result);
    for (int i = 0; i < length; i++) {
        result_ptr[i] = (double)float_data[i + 1];
    }

    free(float_data); 
    Py_DECREF(data_in); 

    return result; // Make sure to return resulting numpy array
}

// Method definition
static PyMethodDef DWTMethods[] = {
    {"call_wt1", py_call_wt1, METH_VARARGS, "Perform wavelet transform on a numpy array"},
    {NULL, NULL, 0, NULL}
};

// Module
static struct PyModuleDef dwtmodule = {
    PyModuleDef_HEAD_INIT,
    "dwt", 
    NULL, 
    -1, 
    DWTMethods
};

// Module initialization
PyMODINIT_FUNC PyInit_dwt(void) {
    import_array(); 
    return PyModule_Create(&dwtmodule);
}