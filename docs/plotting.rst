Plotting results
===============

The RAPID source repository provides ``plot_output.py``, a standalone
Python script for plotting gas and dust snapshots. It does not import
other RAPID scripts and does not require recompiling or rerunning a simulation.
Run the commands below from the directory containing the script.

Installation and input
----------------------

Install NumPy and Matplotlib, and h5py if you use HDF5 output:

.. code-block:: console

   $ python3 -m pip install numpy matplotlib
   $ python3 -m pip install h5py

The input can be a run directory, its ``LOGS`` directory, or an individual
snapshot. ASCII and HDF5 formats are detected automatically. When both formats
exist in the same directory, select one explicitly with ``--format ascii``
or ``--format hdf5``. Gas and dust components are detected from the files.

Profiles and particle positions
-------------------------------

.. code-block:: console

   $ python3 plot_output.py output -o overview.png
   $ python3 plot_output.py output --components dust -o dust.png

The default view shows surface-density profiles coloured by snapshot time,
with the initial and final profiles highlighted. Radius is on the horizontal
axis and surface density on the vertical axis.

For dust, an additional scatter panel shows particle positions: time is on
the horizontal axis, radius on the vertical axis, and colour identifies the
particle ID. These dots show positions, not represented masses or grain sizes.
Gas-only runs have no particle panel. Use ``--no-particles`` for densities only.

Heatmaps
--------

.. code-block:: console

   $ python3 plot_output.py output --kind heatmap -o heatmap.png

Heatmaps show surface density with time horizontally and radius vertically.
Each selected component has its own panel and colourbar. At least two distinct
snapshot times are required. The axes cover the sampled time and radius ranges;
zero-density cells are black.

Initial-density normalization
-----------------------------

To show changes relative to the initial state instead of absolute density:

.. code-block:: console

   $ python3 plot_output.py output --kind heatmap --normalize-initial -o ratio.png

This displays :math:`\Sigma(r,t)/\Sigma(r,0)` separately for each selected
component, using the initial density at the same radius. A ratio of 1 means
unchanged density, 0.5 means half the initial density, and 2 means twice
the initial density.

Normalization also works in the profile view. It requires a saved t=0 snapshot.
Where the initial density is zero, the ratio is undefined: the script warns
and masks those values (black in heatmaps). Without ``--normalize-initial``,
the plots show absolute surface density.

Display options
---------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Option
     - Effect
   * - ``--components gas dust``
     - Select the density components to plot; either can be used alone.
   * - ``--linear``
     - Use linear radius and density scales instead of logarithmic scales.
       Time remains linear.
   * - ``--cmap plasma``
     - Change the density colourmap; the default is ``viridis``.
   * - ``--stride 5``
     - Plot every fifth snapshot, always retaining the final snapshot.
   * - ``--no-particles``
     - Omit particle-position panels in the profile view.
   * - ``--format ascii`` / ``--format hdf5``
     - Select the input format explicitly.
   * - ``-o figure.png``
     - Save the figure; the extension determines the format, including PDF.
       Omit this option to open an interactive window.
   * - ``--help``
     - Display the command-line help.

For example, a normalized dust heatmap with fewer plotted snapshots:

.. code-block:: console

   $ python3 plot_output.py output --kind heatmap --components dust --normalize-initial --stride 5 --cmap plasma -o dust_ratio.pdf

Units and input checks
----------------------

Radius is in AU, time in years, and absolute surface density in solar masses
per AU squared. Normalized densities are dimensionless.

The plotter checks the radial grids, times and density arrays. Missing or
incompatible snapshots produce an explicit error rather than guessing an
older output layout. For static-gas ASCII runs, it uses the saved initial
gas profile. Identical snapshots at the same time are plotted once with
a warning; conflicting snapshots at the same time are rejected.
