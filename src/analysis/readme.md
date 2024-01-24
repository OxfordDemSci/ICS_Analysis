# Analysis

A subdirectory which holds code to conduct our quantitative and computational analyses. To run:

```bash
python make_all_analysis.py
```

A few random points: about this subdirectory:

* Functions in `./src/analysis/figure_plotters/` and `./src/analysis/table_makers` are called by this script to produce the static figures and visualisations.
* These outputs are saved in `./output/figures/` and `./output/tables/` respectively.
* Figures 4-13 and the accompanying summary statistics which go into Section 2 within the Report are powered by the functions within `.`/src/analysis/helpers/cluster_by_cluster.py`.
* Additional helpers are found in the same subdirectory.