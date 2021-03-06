import logging

from pandas import Categorical

from core import prepare
from core import draw

# === helpers === #
BENCH_NAME = 'micro'
EXP_NAME = '%s_perf' % BENCH_NAME
BENCHMARK_ORDER = (
#   "mallocs",
    "arraywrite",
    "arrayread",
    "struct",
    "ptrcreation",
)


def reorder_compilers(df):
    df["compilertype"] = Categorical(df["compilertype"], [
        "gcc-mpx",
        "gcc-mpx_no_narrow_bounds",
        "gcc-mpx_only_write",
        "icc-mpx",
        "icc-mpx_no_narrow_bounds",
        "icc-mpx_only_write",
    ])
    df.sort_values(["compilertype"], inplace=True)


def main(t="perf"):
    logging.info("Processing data")
    df = prepare.process_results(t)
    if t == "perf":
        plot_args = {
            "ylabel": "Normalized runtime\n(w.r.t. native)",
            "ylim"  : (0.9, 6),
            "logy"  : True,
            "ncol"  : 1,
            "build_names": "mpx_feature",
            "figsize"    : (6, 3),
            "legend_loc" : (0.03, 0.6),
        }

        df = prepare.calculate_overhead(df, column="time")
        prepare.reorder_and_rename_benchmarks(df, BENCHMARK_ORDER)
        reorder_compilers(df)

        plot = draw.BarplotMPXFature()
        plot.get_data(df, [], margins=False)
        plot.build_plot(**plot_args)
        plot.save_plot("micro_%s.pdf" % t)

    else:
        logging.error("Unknown plot type")
        exit(-1)
