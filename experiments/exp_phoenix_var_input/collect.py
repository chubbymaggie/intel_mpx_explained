#!/usr/bin/env python
from __future__ import absolute_import

from core import collect as gc


def main():
    full_output_file = gc.data + "/phoenix_var_input/phoenix_var_input.log"
    results_file = gc.data + "/phoenix_var_input/raw.csv"
    gc.collect(results_file, full_output_file)
