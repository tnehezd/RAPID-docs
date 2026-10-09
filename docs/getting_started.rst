Getting started
===============


RAPID can be run either by compiling the source code from the GitHub repository or by installing the pre-built `rapidsim` Python package. Both approaches use the same simulation engine and support configuring simulations through command-line arguments or a YAML configuration file. The Python package provides a convenient way to run simulations without compiling the native code manually.

1. Get the source code
----------------------

The complete RAPID source code is available from the [RAPID GitHub repository](https://github.com/tnehezd/RAPID).

Clone the repository and enter the project directory:

```bash
git clone https://github.com/tnehezd/RAPID.git
cd RAPID
```

To compile the code locally, run:

```bash
make clean
make all
```

This builds the native simulation executable at `bin/simulation`. A compatible C compiler and the dependencies required by the build system must be available in the environment.

2. Run RAPID from the source repository
---------------------------------------

The compiled executable can be run directly using command-line arguments. To display the available options, execute:

```bash
./bin/simulation --help
```

Alternatively, the repository provides a Python wrapper that reads simulation settings from a YAML configuration file and translates them into the command-line arguments expected by the executable. The wrapper requires Python 3.9 or newer and the PyYAML package.

Install the Python dependency if necessary:

```bash
python3 -m pip install PyYAML
```

Then launch a simulation using a configuration file:

```bash
python3 run_simulation.py --config config.yaml
```

The wrapper locates the compiled executable, passes the parameters specified in the YAML file, and streams the simulation output to the terminal.

3. Install the pre-built Python package
---------------------------------------

For users who do not need to modify or compile the source code, RAPID is also available as the `rapidsim` package on PyPI. The package includes the compiled simulation executable and can be installed using:

```bash
python3 -m pip install rapidsim
```

After installation, verify the package version:

```bash
rapidsim --version
```

A simulation can then be launched directly from the command line:

```bash
rapidsim --config config.yaml
```

The PyPI package provides pre-built binaries for supported platforms, eliminating the need to compile RAPID locally. Python 3.9 or newer is required.

4. Configure a simulation
=========================

RAPID can be configured either through a YAML configuration file or directly through command-line switches. The YAML interface groups related parameters into named sections, while direct command-line execution allows individual parameters to be specified when launching the native simulation executable.

YAML configuration
------------------

The YAML configuration file contains the following sections:

* ``simulation_parameters``: simulation processes, fragmentation settings, dust particle count, test mode, and OpenMP thread count.
* ``disk_parameters``: grid properties, initial gas surface density, disk geometry, viscosity, stellar mass, density floors, and photoevaporation settings.
* ``boundary_conditions``: inner and outer boundary conditions.
* ``deadzone_parameters``: dead-zone radii, transition widths, and viscosity reduction.
* ``dust_parameters``: dust-to-gas ratio, particle sizes, population mass ratio, particle density, and smoothing settings.
* ``output_parameters``: output directory and file format.
* ``time_parameters``: time step, total simulation time, and output frequency.
* ``log_parameters``: logging verbosity and terminal status panels.

The following table lists the YAML keys, their corresponding command-line switches, and example values.

.. list-table:: YAML configuration keys and corresponding CLI switches
   :header-rows: 1
   :widths: 40 35 25

   * - YAML section / key
     - CLI switch
     - Example value
   * - ``simulation_parameters.enable_dust_drift``
     - ``-drift``
     - ``true``
   * - ``simulation_parameters.enable_dust_growth``
     - ``-growth``
     - ``true``
   * - ``simulation_parameters.enable_gas_evolution``
     - ``-evol``
     - ``true``
   * - ``simulation_parameters.enable_two_dust_populations``
     - ``-twopop``
     - ``true``
   * - ``simulation_parameters.fragmentation_velocity``
     - ``-ufrag``
     - ``500.0``
   * - ``simulation_parameters.fragmentation_factor``
     - ``-ffrag``
     - ``0.37``
   * - ``simulation_parameters.number_of_dust_particles``
     - ``-ndust``
     - ``1000``
   * - ``simulation_parameters.test_mode``
     - ``--test``
     - ``mass_test``, ``ring_viscosity``, ``photoevap_flux``
   * - ``simulation_parameters.omp_num_threads``
     - ``OMP_NUM_THREADS``
     - ``4``
   * - ``disk_parameters.number_of_grid_points``
     - ``-n``
     - ``500``
   * - ``disk_parameters.radial_grid_type``
     - ``-grid_type``
     - ``linear``, ``logarithmic``
   * - ``disk_parameters.inner_radius_au``
     - ``-ri``
     - ``1.0``
   * - ``disk_parameters.outer_radius_au``
     - ``-ro``
     - ``50.0``
   * - ``disk_parameters.initial_gas_sigma0_msun_per_au2``
     - ``-sigma0_init``
     - ``3.33e-05``
   * - ``disk_parameters.sigma_profile_exponent``
     - ``-index_init``
     - ``-0.5``
   * - ``disk_parameters.alpha_viscosity``
     - ``-alpha_init``
     - ``0.01``
   * - ``disk_parameters.star_mass_msun``
     - ``-stellar_mass``
     - ``1.0``
   * - ``disk_parameters.aspect_ratio_at_1au``
     - ``-h_init``
     - ``0.05``
   * - ``disk_parameters.flaring_index``
     - ``-flind_init``
     - ``0.0``
   * - ``disk_parameters.density_floor``
     - ``-density_floor``
     - ``1e-12``
   * - ``disk_parameters.dust_density_floor``
     - ``-dust_density_floor``
     - ``1e-14``
   * - ``disk_parameters.photoevaporation_mode``
     - ``-photoevap_mode``
     - ``none``, ``owen``, ``picogna``
   * - ``disk_parameters.xray_luminosity_erg_s``
     - ``-xray_luminosity``
     - ``1.0e30``
   * - ``disk_parameters.use_cutoff_for_gas``
     - ``-cutoff``
     - ``false``
   * - ``disk_parameters.characteristic_cutoff_radius_au``
     - ``-cutoff_radius``
     - ``100.0``
   * - ``disk_parameters.cutoff_sharpness_factor``
     - ``-cutoff_sharpness``
     - ``2.0``
   * - ``boundary_conditions.inner_boundary_condition``
     - ``-inner_bc``
     - ``zero_gradient``, ``parabolic``, ``fixed_flux``, ``absorbing``, ``reflecting``
   * - ``boundary_conditions.outer_boundary_condition``
     - ``-outer_bc``
     - ``zero_gradient``, ``parabolic``, ``fixed_flux``, ``absorbing``, ``reflecting``
   * - ``deadzone_parameters.deadzone_inner_radius_au``
     - ``-rdzei``
     - ``2.7``
   * - ``deadzone_parameters.deadzone_outer_radius_au``
     - ``-rdzeo``
     - ``24.0``
   * - ``deadzone_parameters.deadzone_inner_transition_width_mult``
     - ``-drdzei``
     - ``0.5``
   * - ``deadzone_parameters.deadzone_outer_transition_width_mult``
     - ``-drdzeo``
     - ``0.5``
   * - ``deadzone_parameters.deadzone_alpha_reduction``
     - ``-amod``
     - ``0.01``
   * - ``dust_parameters.initial_dust_to_gas_ratio``
     - ``-eps``
     - ``0.01``
   * - ``dust_parameters.population_one_mass_ratio``
     - ``-ratio``
     - ``0.85``
   * - ``dust_parameters.micro_particle_size_cm``
     - ``-micsize``
     - ``0.0001``
   * - ``dust_parameters.one_size_particle_value_cm``
     - ``-largesize``
     - ``1.0``
   * - ``dust_parameters.dust_particle_density_g_cm3``
     - ``-pdensity``
     - ``1.6``
   * - ``dust_parameters.disk_mass_dust``
     - ``-disk_mass``
     - ``0.01``
   * - ``dust_parameters.dust_smoothing_mode``
     - ``-dust_smoothing``
     - ``cic``, ``ngp``, ``tophat``, ``gaussian``
   * - ``dust_parameters.gaussian_smoothing_sigma_grid_units``
     - ``-gaussian_sigma_grid_units``
     - ``1.0``
   * - ``dust_parameters.gaussian_smoothing_cutoff_sigma``
     - ``-gaussian_cutoff_sigma``
     - ``3.0``
   * - ``output_parameters.output_directory_name``
     - ``-o``
     - ``output``
   * - ``output_parameters.output_format``
     - ``-output_format``
     - ``ascii``, ``hdf5``
   * - ``time_parameters.fixed_time_step``
     - ``-tStep``
     - ``0.0``
   * - ``time_parameters.total_simulation_time``
     - ``-tmax``
     - ``5e5``
   * - ``time_parameters.output_write_frequency``
     - ``-outfreq``
     - ``1000``
   * - ``log_parameters.info_level``
     - ``-v`` / ``-vv``
     - ``none``, ``info``, ``debug``
   * - ``log_parameters.disable_terminal_panels``
     - ``-no_panels``
     - ``false``

To run a simulation using a YAML configuration file, execute:

.. code-block:: bash

   rapidsim --config config.yaml

When running from the source repository, use the Python wrapper instead:

.. code-block:: bash

   python3 run_simulation.py --config config.yaml

Replace ``config.yaml`` with the path to the desired configuration file.

Direct command-line execution
-----------------------------

The native simulation executable can also be run directly, without a YAML file or the Python wrapper. For example, the following command enables dust drift, dust growth, gas evolution, and two dust populations:

.. code-block:: bash

   ./bin/simulation -drift 1 -growth 1 -evol 1 -twopop 1

To display all available command-line options, run:

.. code-block:: bash

   ./bin/simulation --help

The complete list of command-line switches, descriptions, default values, and units is provided in the command-line reference.


5. Output and further documentation
-----------------------------------

After a simulation finishes, RAPID writes the results to the output directory specified in the configuration file. Depending on the selected output format, the simulation snapshots are stored as ASCII text files or HDF5 files. Diagnostic and runtime information is also generated.

For more information about the simulation parameters, output files, example configurations, and benchmark tests, consult the [RAPID documentation](https://rapiddocs.readthedocs.io/en/latest/).