from cx_Freeze import setup, Executable
import os, sys

exe = Executable(
    "mainwindow.py",
    includes="BoPunk",
    path=[os.path.abspath("src"),]
)

setup(
        name = "hello",
        version = "0.1",
        description = "the typical 'Hello, world!' script",
        executables = [exe],
)