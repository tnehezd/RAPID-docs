rapidsim
========

``rapidsim`` is a Python interface to the **RAPID simulation engine**, not
a separate physical model. It provides a packaged native executable,
single-run launching from YAML or Python, and parameter-grid orchestration.
The gas and dust equations are described in :doc:`physical_background`;
the numerical methods are described in :doc:`numerical_impl`.

RAPID versus rapidsim
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Feature
     - RAPID source repository
     - rapidsim package
   * - Simulation engine
     - Locally compiled ``bin/simulation``
     - Packaged RAPID executable
   * - YAML launcher
     - ``python3 run_simulation.py --config FILE``
     - ``rapidsim --config FILE``
   * - Python interface
     - Source wrapper
     - ``run()`` and ``run_grid()``
   * - Parameter grids
     - Source launcher expects scalar parameters
     - List-valued parameters launch multiple runs

The package and native engine have separate version identifiers.
``rapidsim --version`` reports the package version, not necessarily the
RAPID engine version. Check the native startup banner or
``current_run_info.dat`` for the engine used in a calculation.
Updating the Python wrapper does not replace a bundled executable.

.. important::

   The grid features below describe the current rapidsim wrapper source.
   An installed PyPI release may provide an older interface or RAPID binary.
   Use a compatible package release; do not assume that every development
   option is available in a previously installed package.

Installation and a single run
-----------------------------

The package requires Python 3.8 or newer and includes native binaries for
supported platforms:

.. code-block:: console

   $ python3 -m pip install rapidsim
   $ rapidsim --version
   $ rapidsim --config config.yaml

The configuration file must already exist; installation does not create it.
For compiling RAPID yourself, see :doc:`getting_started`.

A minimal gas-only configuration can be saved as ``config.yaml``:

.. code-block:: yaml

   simulation_parameters:
     enable_gas_evolution: true
     enable_dust_drift: false
     enable_dust_growth: false
     omp_num_threads: 1
   disk_parameters:
     number_of_grid_points: 100
     inner_radius_au: 1.0
     outer_radius_au: 50.0
     disk_mass: 0.01
     sigma_profile_exponent: -1.0
     alpha_viscosity: 0.001
   time_parameters:
     total_simulation_time: 1000.0
     output_write_frequency: 100
   output_parameters:
     output_directory_name: gas_run
     output_format: ascii

The same run can be launched from Python:

.. code-block:: python

   from rapidsim import run

   result = run("config.yaml")
   print(result.returncode)

``run()`` also accepts a Python dictionary with the same configuration sections.
Its ``output_dir`` argument overrides the configured output directory:

.. code-block:: python

   import yaml
   from rapidsim import run

   with open("config.yaml") as stream:
       config = yaml.safe_load(stream)
   result = run(config, output_dir="another_gas_run")

YAML parameter grids
--------------------

Put lists directly on the parameters to vary, in their usual sections.
For example, replace ``alpha_viscosity`` and ``sigma_profile_exponent``
in the configuration above with:

.. code-block:: yaml

   disk_parameters:
     number_of_grid_points: 100
     inner_radius_au: 1.0
     outer_radius_au: 50.0
     disk_mass: 0.01
     alpha_viscosity: [0.001, 0.01]
     sigma_profile_exponent: [-0.5, -1.0]
   grid_options:
     output_directory: gas_grid
     max_workers: 2

Retain the other sections from the single-run configuration.
Then use the same command:

.. code-block:: console

   $ rapidsim --config config.yaml

The wrapper automatically launches **four runs**, one for every combination
of the two viscosity values and two profile exponents. Scalar parameters stay
fixed. A one-element list is treated as a scalar by ``run()`` and the CLI.
There is no separate CLI grid switch.

Python grids and paired values
-----------------------------

The same automatic grid behavior is available through ``run()``:

.. code-block:: python

   from rapidsim import run

   results = run("config.yaml", output_dir="gas_grid")
   for result in results:
       print(result.parameters, result.output_dir, result.process.returncode)

Alternatively, keep ``config.yaml`` scalar and pass the varied parameters
explicitly to ``run_grid()``:

.. code-block:: python

   from rapidsim import run_grid

   results = run_grid(
       "config.yaml",
       parameter_grid={
           "disk_parameters.alpha_viscosity": [0.001, 0.01],
           "disk_parameters.sigma_profile_exponent": [-0.5, -1.0],
       },
       output_dir="gas_grid",
       max_workers=2,
   )

This also launches four combinations. Do not combine an explicit
``parameter_grid`` argument with list-valued parameters in the configuration.

To pair the values by index instead of forming every combination, add
``mode="paired"`` to the ``run_grid()`` call. The example then launches
**two runs**: ``(0.001, -0.5)`` and ``(0.01, -1.0)``. Lists must have
equal lengths, except that one-element lists are broadcast. Paired mode
is selected through the Python API, not ``grid_options``.

Outputs, concurrency and errors
------------------------------

Each grid member writes to its own subdirectory. Process output is saved
in the grid root's ``logs/run_NNNN.log`` files. If the grid output root already
exists, the wrapper chooses a new numbered root instead of overwriting it.
This protection is specific to grid roots; do not assume that a single run
has the same directory-renaming behavior.

``max_workers`` limits concurrent simulations. ``omp_num_threads`` in
``simulation_parameters`` controls threads within each native process.
For example, two workers with one OpenMP thread each run two simulations
concurrently. Choose both limits to avoid oversubscribing the machine.

A single ``run()`` returns a ``subprocess.CompletedProcess``.
Grid calls return a list of ``GridRunResult`` objects, with ``parameters``,
``output_dir``, ``process`` and ``log_file`` attributes.
By default, failed single runs raise ``subprocess.CalledProcessError`` and
failed grids raise ``GridRunError``. With ``check=False``, inspect the
returned process exit codes yourself. The CLI returns a nonzero exit code
when a simulation fails.

Plotting and shared settings
---------------------------

The YAML physics settings map to the same RAPID switches described in
:doc:`getting_started`. The rapidsim wrapper additionally supports
``grid_options`` and the Python orchestration arguments above.
Single-population dust carries the full initialized dust mass.

Snapshots use the RAPID output formats. The standalone source-repository
``plot_output.py`` can plot an individual grid member's output directory;
it is not installed as a rapidsim command. See :doc:`plotting` for profile
plots, heatmaps and initial-density normalization.
