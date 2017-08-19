# How to turn data in beautiful, interactive visualizations

This is a short introductory tutorial regarding creating visualizations in bokeh. This tutorial is divided into two parts. We will start with a generic introduction to bokeh based on [bokeh's notebooks](https://github.com/bokeh/bokeh-notebooks/blob/master/index.ipynb). Then we will proceed with two examples:
- [eclipse.py](eclipse.py) &mdash; visualization of the relationship between popularity of "solar eclipse" term in Google Search across contiguous United States and the path of total solar eclipse of 2017,
- [sprint.py](sprint.py) &mdash; visualization of the history of olympic medals in 100 meter dash in the context of Usain Bolt's 2012 olympic record of 9.63 seconds.

# Prerequisites

You will need to install `bokeh`, `pandas` and `pyshp` to run code included in this tutorial. It would be also useful to use Jupyter as the interactive environment. You can install these packages the way you like, though the most efficient and reliable is to use either [Anaconda](https://www.continuum.io/downloads) distribution or [Miniconda](https://conda.io/miniconda.html) (which is preferred for this tutorial due to its smaller footprint).

Download an installer for your system and follow the instructions. When done, proceed with:
```
$ conda create -n pycon-bokeh python=3 bokeh pandas jupyter
$ conda install -n pycon-bokeh -c conda-forge pyshp
```

This will create an environment named `pycon-bokeh` with most recent version of Python 3 and selected libraries installed in it. Note that we have to install `pyshp` from `conda-forge` channel, which contains official community driven packages.

To activate `pycon-bokeh` issue:
```
$ source activate pycon-bokeh
```
or
```
$ activate pycon-bokeh
```
on Windows. To test if everything works, issue:
```
$ python -c "import bokeh; print(bokeh.__version__)"
```
which should give you `0.12.6`.