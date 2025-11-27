from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "neuronet",
        sources=["cython_layer/neuronet.pyx", "cpp/GrafoDisperso.cpp"],
        language="c++",
        extra_compile_args=["-std=c++11"],
        include_dirs=["cpp"]
    )
]

setup(
    name="neuronet",
    ext_modules=cythonize(extensions),
)
