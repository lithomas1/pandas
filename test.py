import numba
import numpy as np

import pandas as pd
import pandas.core._numba.extensions


@numba.njit
def test_recarray(df):
    # print(df["a"])
    # return df._values#['a']
    return df._values
    # print(df)
    # return df


@numba.njit
def test_df(df):
    # print(df["a"])
    # return df._values#['a']
    return df
    # print(df)
    # return df


@numba.njit
def test_df_indexing(df):
    return df["a"]


# @numba.njit
# def test_df_col_to_np(df):
#     return np.array(df['a'])


@numba.extending.intrinsic
def address_as_void_pointer(typingctx, src):
    """returns a void pointer from a given memory address"""
    from numba.core import (
        cgutils,
        types,
    )

    sig = types.voidptr(src)

    def codegen(cgctx, builder, sig, args):
        return builder.inttoptr(args[0], cgutils.voidptr_t)

    return sig, codegen


@numba.njit
def test_recarray1(arr):
    # print(arr['a'].sum())
    return arr[0]


@numba.njit
def test_recarray_df_constructor(arr):
    print(arr)
    # data = numba.carray(address_as_void_pointer(arr.ctypes.data), arr.shape, dtype=arr.dtype)
    # print(data)
    df = pd.DataFrame(
        arr, index=pd.Index(np.array([1, 2, 3])), columns=numba.typed.List([0, 1])
    )
    # df = pd.DataFrame(data, index=pd.Index(np.array([1, 2, 3])), columns=numba.typed.List([0, 1]))
    print(df._values)
    print(df._values.ctypes.data)
    print(df._values.shape)
    # print(df._values['a'])
    # return df._values


df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
arr = np.rec.fromarrays(df._mgr.column_arrays, None, None, None, df.columns.tolist())
# print(test_recarray1(arr))
# arr_res = test_recarray1(arr)
# print(arr_res)
# res = test_recarray(df)
# print(res)
# print(res.itemsize)
res = test_recarray_df_constructor(arr)
# print(res)
# print(res.dtype)
# print(test_recarray_df_constructor(arr))
