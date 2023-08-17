"""
Utility classes/functions to let numba recognize
pandas Index/Series/DataFrame

Mostly vendored from https://github.com/numba/numba/blob/main/numba/tests/pdlike_usecase.py
"""

from __future__ import annotations

import numba
from numba.core import (
    cgutils,
    types,
)
from numba.core.datamodel import models
from numba.core.extending import (
    NativeValue,
    box,
    lower_builtin,
    make_attribute_wrapper,
    register_model,
    type_callable,
    typeof_impl,
    unbox,
)
from numba.core.imputils import impl_ret_borrowed
from numba.np.arrayobj import make_array
import numpy as np

from pandas.core.frame import DataFrame
from pandas.core.indexes.base import Index


# TODO: Range index support
# (not passing an index to series constructor doesn't work)
class IndexType(types.Buffer):
    """
    The type class for Index objects.
    """

    array_priority = 1000

    def __init__(self, dtype, layout, pyclass) -> None:
        self.pyclass = pyclass
        super().__init__(dtype, 1, layout)

    @property
    def key(self):
        return self.pyclass, self.dtype, self.layout

    @property
    def as_array(self):
        return types.Array(self.dtype, 1, self.layout)

    def copy(self, dtype=None, ndim: int = 1, layout=None):
        assert ndim == 1
        if dtype is None:
            dtype = self.dtype
        layout = layout or self.layout
        return type(self)(dtype, layout, self.pyclass)


# class SeriesType(types.ArrayCompatible):
# class SeriesType(types.Type):
#     """
#     The type class for Series objects.
#     """
#
#     array_priority = 1000
#
#     def __init__(self, dtype, index) -> None:
#         assert isinstance(index, IndexType)
#         self.dtype = dtype
#         self.index = index
#         self.values = types.Array(self.dtype, 1, "C")
#         name = f"series({dtype}, {index})"
#         super().__init__(name)
#
#     @property
#     def key(self):
#         return self.dtype, self.index
#
#     @property
#     def as_array(self):
#         return self.values
#
#     def copy(self, dtype=None, ndim: int = 1, layout: str = "C"):
#         assert ndim == 1
#         assert layout == "C"
#         if dtype is None:
#             dtype = self.dtype
#         return type(self)(dtype, self.index)


# class DataFrameType(types.Type):
#     """
#     The type class for DataFrame objects.
#     """
#
#     array_priority = 1000
#
#     def __init__(self, dtype, index, layout, columns) -> None:
#         assert isinstance(index, IndexType)
#         self.dtype = dtype
#         self.index = index
#         self.layout = layout
#         self.values = types.Array(self.dtype, 2, layout)
#         self.columns = columns
#         name = f"dataframe({dtype}, {index}, {layout}, {columns})"
#         super().__init__(name)
#
#     @property
#     def key(self):
#         return self.dtype, self.index, self.layout, self.columns
#
#     @property
#     def as_array(self):
#         return self.values
#
#     def copy(self, dtype=None, ndim: int = 2, layout: str = "F"):
#         assert ndim == 2
#         if dtype is None:
#             dtype = self.dtype
#         return type(self)(dtype, self.index, layout, self.columns)


class DataFrameType(types.Type):
    def __init__(self, values_dtype, index, columns) -> None:
        self.values_dtype = values_dtype
        self.index = index
        self.columns = columns
        name = f"dataframe({self.values_dtype}, {index}, {columns})"
        super().__init__(name)

    @property
    def key(self):
        return self.values_dtype, self.index, self.columns


@typeof_impl.register(Index)
def typeof_index(val, c):
    arrty = typeof_impl(val._data, c)
    assert arrty.ndim == 1
    return IndexType(arrty.dtype, arrty.layout, type(val))


# @typeof_impl.register(Series)
# def typeof_series(val, c):
#     index = typeof_impl(val.index, c)
#     arrty = typeof_impl(val.values, c)
#     assert arrty.ndim == 1
#     assert arrty.layout == "C"
#     return SeriesType(arrty.dtype, index)


@typeof_impl.register(DataFrame)
def typeof_df(val, c):
    index = typeof_impl(val.index, c)
    # arrty = typeof_impl(val.values, c)

    vals_dtype_dict = val.dtypes.to_dict()
    vals_np_dtype = np.dtype([(name, dtype) for name, dtype in vals_dtype_dict.items()])

    vals_nb_dtype = numba.np.numpy_support.from_struct_dtype(vals_np_dtype)
    vals_dtype = types.Array(vals_nb_dtype, 1, "C", aligned=False)

    dtype = val.columns.dtype
    if dtype == object:
        dtype = types.unicode_type
    else:
        dtype = numba.from_dtype(dtype)
    colty = types.ListType(dtype)
    return DataFrameType(vals_dtype, index, colty)


# @type_callable("__array_wrap__")
# def type_array_wrap(context):
#     def typer(input_type, result):
#         if isinstance(input_type, (IndexType, SeriesType)):
#             return input_type.copy(
#                 dtype=result.dtype, ndim=result.ndim, layout=result.layout
#             )
#
#     return typer


# @type_callable(Series)
# def type_series_constructor(context):
#     def typer(data, index):
#         if isinstance(index, IndexType) and isinstance(data, types.Array):
#             assert data.layout == "C"
#             assert data.ndim == 1
#             return SeriesType(data.dtype, index)
#
#     return typer


@type_callable(Index)
def type_index_constructor(context):
    def typer(data):
        if isinstance(data, types.Array):
            assert data.layout == "C"
            assert data.ndim == 1
            return IndexType(data.dtype, layout=data.layout, pyclass=Index)

    return typer


@type_callable(DataFrame)
def type_frame_constructor(context):
    def typer(data, index=None, columns=None):
        # TODO: Can I overload this with multiple isinstance
        if (
            isinstance(data, types.Array)
            and isinstance(index, IndexType)
            and isinstance(columns, types.ListType)
        ):
            assert isinstance(data.dtype, types.Record)

            return DataFrameType(data, index, columns)
        elif isinstance(data, types.Array) and index is None:
            assert isinstance(data.dtype, types.Record)

            # If no index, it will be a "RangeIndex"
            # TODO: get rid of columns argument here
            return DataFrameType(
                data,
                IndexType(numba.int64, "C", Index),
                types.ListType(types.unicode_type),
            )

        elif isinstance(data, DataFrameType):
            return DataFrameType(data.values_dtype, data.index, data.columns)

        # if isinstance(index, IndexType) and isinstance(data, types.Array):
        #     assert data.ndim == 2
        #     if columns is None:
        #         columns = types.ListType(types.int64)
        #     assert isinstance(columns, types.ListType) and (
        #         columns.dtype is types.unicode_type or types.Integer
        #     )
        #     return DataFrameType(data.dtype, index, data.layout, columns)

    return typer


# Backend extensions for Index and Series and Frame
@register_model(IndexType)
class IndexModel(models.StructModel):
    def __init__(self, dmm, fe_type) -> None:
        members = [("data", fe_type.as_array)]
        models.StructModel.__init__(self, dmm, fe_type, members)


# @register_model(SeriesType)
# class SeriesModel(models.StructModel):
#     def __init__(self, dmm, fe_type) -> None:
#         members = [
#             ("index", fe_type.index),
#             ("values", fe_type.as_array),
#         ]
#         models.StructModel.__init__(self, dmm, fe_type, members)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):
    def __init__(self, dmm, fe_type) -> None:
        members = [
            ("index", fe_type.index),
            ("values", fe_type.values_dtype),
            ("columns", fe_type.columns),
        ]
        models.StructModel.__init__(self, dmm, fe_type, members)


make_attribute_wrapper(IndexType, "data", "_data")

# make_attribute_wrapper(SeriesType, "index", "index")
# make_attribute_wrapper(SeriesType, "values", "values")

make_attribute_wrapper(DataFrameType, "index", "index")
make_attribute_wrapper(DataFrameType, "values", "_values")
# make_attribute_wrapper(DataFrameType, "values_ptr", "_values_ptr")
make_attribute_wrapper(DataFrameType, "columns", "columns")


# @lower_builtin("__array__", IndexType)
# def index_as_array(context, builder, sig, args):
#     val = cgutils.create_struct_proxy(sig.args[0])(context, builder, ref=args[0])
#     return val._get_ptr_by_name("data")
#
#
# @lower_builtin("__array__", SeriesType)
# def series_as_array(context, builder, sig, args):
#     val = cgutils.create_struct_proxy(sig.args[0])(context, builder, ref=args[0])
#     return val._get_ptr_by_name("values")


# @lower_builtin(Series, types.Array, IndexType)
# def pdseries_constructor(context, builder, sig, args):
#     data, index = args
#     series = cgutils.create_struct_proxy(sig.return_type)(context, builder)
#     series.index = index
#     series.values = data
#     return impl_ret_borrowed(context, builder, sig.return_type, series._getvalue())


@lower_builtin(Index, types.Array)
def index_constructor(context, builder, sig, args):
    (data,) = args
    index = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    index.data = data
    return impl_ret_borrowed(context, builder, sig.return_type, index._getvalue())


# TODO: can we mix low level and high level numba extension APIs here
# e.g. overload(DataFrame) that calls down into a lower_builtin wrapped
# function to create the struct?

# @lower_builtin(DataFrame, types.Array, IndexType)
# def pdframe_constructor(context, builder, sig, args):
#     data, index, columns = args
#     df = cgutils.create_struct_proxy(sig.return_type)(context, builder)
#     # df.index = index
#     # df._values = data
#     # df.columns = columns
#     return impl_ret_borrowed(context, builder, sig.return_type, df._getvalue())


@lower_builtin(DataFrame, types.Array, IndexType, types.ListType)
def pdframe_constructor1(context, builder, sig, args):
    with open("1.txt", "w") as f:
        f.write(str(builder.module))
    # print(builder.module)
    data, index, columns = args
    df = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    ary = make_array(sig.args[0])(context, builder, value=data)
    df_ary = make_array(sig.args[0])(context, builder, value=df.values)
    context.nrt.incref(builder, sig.args[0], data)
    df.index = index
    cgutils.copy_struct(df_ary, ary)  # data #ary.data
    df.columns = columns
    ret = df._getvalue()
    with open("2.txt", "w") as f:
        f.write(str(builder.module))
    return ret
    # return impl_ret_untracked(context, builder, sig.return_type, df._getvalue())


@unbox(IndexType)
def unbox_index(typ, obj, c):
    """
    Convert a Index object to a native structure.
    """
    data_obj = c.pyapi.object_getattr_string(obj, "_data")
    index = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    index.data = c.unbox(typ.as_array, data_obj).value

    # Decrefs
    c.pyapi.decref(data_obj)

    return NativeValue(index._getvalue())


# @unbox(SeriesType)
# def unbox_series(typ, obj, c):
#     """
#     Convert a Series object to a native structure.
#     """
#     index_obj = c.pyapi.object_getattr_string(obj, "index")
#     values_obj = c.pyapi.object_getattr_string(obj, "values")
#     series = cgutils.create_struct_proxy(typ)(c.context, c.builder)
#     series.index = c.unbox(typ.index, index_obj).value
#     series.values = c.unbox(typ.values, values_obj).value
#
#     # Decrefs
#     c.pyapi.decref(index_obj)
#     c.pyapi.decref(values_obj)
#
#     return NativeValue(series._getvalue())


@unbox(DataFrameType)
def unbox_df(typ, obj, c):
    """
    Convert a DataFrame object to a native structure.
    """
    # TODO: Check refcounting!!!
    index_obj = c.pyapi.object_getattr_string(obj, "index")
    # values_obj = c.pyapi.object_getattr_string(obj, "values")

    mgr = c.pyapi.object_getattr_string(obj, "_mgr")
    col_arrays = c.pyapi.object_getattr_string(mgr, "column_arrays")

    columns_index_obj = c.pyapi.object_getattr_string(obj, "columns")

    columns_list_obj = c.pyapi.call_method(columns_index_obj, "tolist")

    # Create recarray from df
    recarray = c.pyapi.unserialize(c.pyapi.serialize_object(np.rec.fromarrays))
    recarray_obj = c.pyapi.call_function_objargs(
        # TODO: Is the borrowing of None here safe?
        recarray,
        (
            col_arrays,
            c.pyapi.borrow_none(),
            c.pyapi.borrow_none(),
            c.pyapi.borrow_none(),
            columns_list_obj,
        ),
    )

    typed_list = c.pyapi.unserialize(c.pyapi.serialize_object(numba.typed.List))

    df = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    df.index = c.unbox(typ.index, index_obj).value
    # df.values = c.unbox(typ.values, values_obj).value
    # print(typ.values_dtype)
    df._values = c.unbox(typ.values_dtype, recarray_obj).value

    # Convert to numba typed list
    columns_typed_list_obj = c.pyapi.call_function_objargs(
        typed_list, (columns_list_obj,)
    )
    df.columns = c.unbox(typ.columns, columns_typed_list_obj).value

    # Decrefs
    c.pyapi.decref(recarray_obj)

    c.pyapi.decref(index_obj)
    # c.pyapi.decref(values_obj)
    c.pyapi.decref(columns_index_obj)
    c.pyapi.decref(columns_list_obj)
    c.pyapi.decref(columns_typed_list_obj)

    return NativeValue(df._getvalue())


@box(IndexType)
def box_index(typ, val, c):
    """
    Convert a native index structure to a Index object.
    """
    # First build a Numpy array object, then wrap it in a Index
    index = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val)
    class_obj = c.pyapi.unserialize(c.pyapi.serialize_object(typ.pyclass))
    array_obj = c.box(typ.as_array, index.data)
    index_obj = c.pyapi.call_function_objargs(class_obj, (array_obj,))

    # Decrefs
    c.pyapi.decref(class_obj)
    c.pyapi.decref(array_obj)
    return index_obj


# @box(SeriesType)
# def box_series(typ, val, c):
#     """
#     Convert a native series structure to a Series object.
#     """
#     series = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val)
#     class_obj = c.pyapi.unserialize(c.pyapi.serialize_object(Series))
#     index_obj = c.box(typ.index, series.index)
#     array_obj = c.box(typ.as_array, series.values)
#     series_obj = c.pyapi.call_function_objargs(class_obj, (array_obj, index_obj))
#
#     # Decrefs
#     c.pyapi.decref(class_obj)
#     c.pyapi.decref(index_obj)
#     c.pyapi.decref(array_obj)
#
#     return series_obj


@box(DataFrameType)
def box_df(typ, val, c):
    """
    Convert a native series structure to a DataFrame object.
    """
    df = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val)
    class_obj = c.pyapi.unserialize(c.pyapi.serialize_object(DataFrame))
    indexclass_obj = c.pyapi.unserialize(c.pyapi.serialize_object(Index))
    index_obj = c.box(typ.index, df.index)
    array_obj = c.box(typ.values_dtype, df.values)

    columns_obj = c.box(typ.columns, df.columns)
    columns_index_obj = c.pyapi.call_function_objargs(indexclass_obj, (columns_obj,))

    df_obj = c.pyapi.call_function_objargs(
        # class_obj, (array_obj, index_obj, columns_index_obj)
        class_obj,
        (array_obj, index_obj),
    )

    # Decrefs
    c.pyapi.decref(class_obj)
    c.pyapi.decref(indexclass_obj)
    c.pyapi.decref(index_obj)
    c.pyapi.decref(array_obj)
    c.pyapi.decref(columns_obj)
    c.pyapi.decref(columns_index_obj)

    return df_obj


# binops = [operator.add, operator.sub, operator.mul, operator.truediv]


# def _generate_series_binop(op):
#     def series_op(self, other):
#         if isinstance(self, SeriesType) and isinstance(other, SeriesType):
#             return lambda self, other: Series(
#                 op(self.values, other.values), index=self.index
#             )
#
#     return series_op


# for op in binops:
#     overload(op)(_generate_series_binop(op))

# @overload(operator.getitem)
# def df_getitem(self, colname):
#     if isinstance(self, DataFrameType):
#         return lambda self, colname: Series(
#             self._values[colname], self.index
#         )
