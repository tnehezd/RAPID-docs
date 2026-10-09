Getting started
===============


``RAPID`` can be run either by compiling the source code from the GitHub repository or by installing the pre-built `rapidsim` Python package. Both approaches use the same simulation engine and support configuring simulations through command-line arguments or a YAML configuration file. The Python package provides a convenient way to run simulations without compiling the native code manually.

1. Get the source code from GitHub
----------------------------------

The complete RAPID source code is available from the `RAPID GitHub repository <https://github.com/tnehezd/RAPID>`_.

Clone the repository and enter the project directory:


.. code-block:: console

  $ git clone https://github.com/tnehezd/RAPID.git
  $ cd RAPID


To compile the code locally, run:

.. code-block:: console

  $ make clean
  $ make all

This builds the native simulation executable at `bin/simulation`. A compatible C compiler and the dependencies required by the build system must be available in the environment.

I. Run RAPID from the source repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The compiled executable can be run directly using command-line arguments. To display the available options, execute:

.. code-block:: console

  $ ./bin/simulation --help


The native simulation executable can be run directly. For example, the following command enables dust drift, dust growth, gas evolution, and two dust populations:

.. code-block:: bash

   ./bin/simulation -drift 1 -growth 1 -evol 1 -twopop 1

To display all available command-line options, run:

.. code-block:: bash

   ./bin/simulation --help

The complete list of command-line switches, descriptions, default values, and units is provided in Table :ref:`yaml_configuration_keys`.

----

Alternatively, the repository provides a Python wrapper that reads simulation settings from a YAML configuration file and translates them into the command-line arguments expected by the executable. The wrapper requires Python 3.9 or newer and the PyYAML package.

Install the Python dependency if necessary:

.. code-block:: console

  $ python3 -m pip install PyYAML

Then launch a simulation using a configuration file:

.. code-block:: console

  $ python3 run_simulation.py --config config.yaml

The wrapper locates the compiled executable, passes the parameters specified in the YAML file, and executes the simulation, outputting the results to the terminal and to the specified output directory.

----

2. Install the ``rapidsim`` Python package
---------------------------------------

For users who do not need to modify or compile the source code, ``RAPID`` is also available as the `rapidsim` package on PyPI. The package includes the compiled simulation executable and can be installed using:

.. code-block:: console

  $ python3 -m pip install rapidsim

After installation, verify the package version:

.. code-block:: console

  $ rapidsim --version

A simulation can then be launched directly from the command line:

.. code-block:: console

  $ rapidsim --config config.yaml

The PyPI package provides pre-built binaries for supported platforms, eliminating the need to compile RAPID locally. Python 3.9 or newer is required.


Understanding YAML configuration files
======================================

``RAPID`` can be configured either through a YAML configuration file or directly through command-line switches. The YAML interface groups related parameters into named sections, while direct command-line execution allows individual parameters to be specified when launching the native simulation executable.

YAML configuration
~~~~~~~~~~~~~~~~~~

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
   :name: yaml_configuration_keys
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

A typical YAML configuration file should be structured in a nested format as follows:

.. code-block:: yaml
    # example YAML config file

    simulation_parameters:
        # Simulation Control Options 
        enable_dust_drift:           false     
        enable_dust_growth:          false     
        enable_gas_evolution:        true    
        enable_two_dust_populations: false 
        enable_photoevaporation:     false      
        
    disk_parameters:
        # Grid and Disk Initial Parameters 
        number_of_grid_points:   500    
        inner_radius_au:         1           
        outer_radius_au:         50.0         
        disk_mass:               0.01              
        sigma_profile_exponent: -1.0  
        alpha_viscosity:         0.01      
        aspect_ratio_at_1au:     0.05    

    output_parameters:
        # File I/O Parameters
        output_directory_name: "output"    
        output_format:         "ascii"               

    time_parameters:
        # Time Parameters
        total_simulation_time:  1e5       
        output_write_frequency: 1000
            

To run a simulation using a YAML configuration file, execute:

.. code-block:: bash

   rapidsim --config config.yaml

When running from the source repository, use the Python wrapper instead:

.. code-block:: bash

   python3 run_simulation.py --config config.yaml

Replace ``config.yaml`` with the path to the desired configuration file.


5. Expected output
------------------


Upon successful execution, ``RAPID`` prints an initialization summary and a live progress panel to the terminal. These report the code version, the active physical modules, the main disk and dust parameters, the current simulation time, the time step, and the disk mass. The verbosity can be controlled using the ``info_level`` setting in the YAML configuration file (``none``, ``info``, or ``debug``). For notebook-based execution, the terminal panels can be disabled by setting:

.. code-block:: yaml

   log_parameters:
     disable_terminal_panels: true

A typical initialization output is shown in Figure :ref:`rapid_init_output`. During the main simulation loop, RAPID displays a live progress panel, as illustrated for a pure-gas accretion run in Figure :ref:`main_loop` in Appendix :ref:`terminal_outputs`. The panel is updated as the simulation advances, with output corresponding to the snapshots written during the run. The output frequency is controlled by ``output_write_frequency`` in the YAML configuration or the ``-outfreq`` command-line option.

Figure :ref:`benchmark_terminal` shows the terminal output of a benchmark test run without the real-time status panel. Benchmark output differs slightly from that of standard simulations: it explicitly identifies the active test and highlights physical modules that are disabled or overridden for the benchmark. The ``ring_test.ipynb`` notebook, available in the GitHub repository and the official documentation, provides an example of benchmark analysis.

Output files are written to the directory specified by the ``-o`` command-line option or the ``output_directory_name`` YAML setting. A typical output directory contains the following:

* ``config/`` — processed configuration files, including ``disk_config.dat``, ``initial_gas_profile.dat``, and, when applicable, ``initial_dust_profile.dat``.
* ``LOGS/`` — diagnostic files and simulation snapshots.
* ``current_run_info.dat`` — metadata describing the simulation.
* ``current_runtime_performance_info.dat`` — timing and performance statistics.

The exact files in ``LOGS/`` depend on the selected output format and the active physical modules. For example, HDF5 output may contain files such as:

.. code-block:: text

   snapshot_00000000.h5
   snapshot_00010000.h5
   snapshot_00020000.h5
   ...
   snapshot_00090000.h5
   ...
   mass_accumulation_dze_edge.h5

ASCII output may contain files such as:

.. code-block:: text

   density_profile_00000000.dat
   dust_size_evolution_00000000.dat
   dust_density_profile_00000000.dat
   micron_dust_size_evolution_00000000.dat
   dust_micron_density_profile_00000000.dat
   ...
   density_profile_00090000.dat
   dust_size_evolution_00090000.dat
   dust_density_profile_00090000.dat
   micron_dust_size_evolution_00090000.dat
   dust_micron_density_profile_00090000.dat
   ...

The ``ascii`` output format stores radial profiles as plain numerical text files that can be inspected with a text editor or processed using standard command-line tools. The ``hdf5`` format stores the simulation state in a structured binary format, allowing compact storage and efficient access to individual datasets during post-processing.

In the current version, benchmark runs generate ASCII profile files and a summary file. For example, a ring-viscosity benchmark may produce:

.. code-block:: text

   ring_profile_t_000000.dat
   ring_profile_t_020000.dat
   ...
   ring_viscous_summary.dat

Benchmark output files can be read directly by the analysis notebooks provided with RAPID.

HDF5 snapshot structure
-----------------------

When ``output_format`` is set to ``hdf5``, RAPID writes each snapshot to a structured HDF5 file containing the disk state at a particular simulation time. A representative snapshot, ``snapshot_00000000.h5``, with 1000 grid cells and 5000 particles, contains the groups and datasets listed in Table :ref:`hdf5_snapshot_structure`.

.. list-table:: Dataset structure of a representative RAPID HDF5 snapshot (``snapshot_00000000.h5``).
   :name: hdf5_snapshot_structure
   :header-rows: 1
   :widths: 20 25 45 10

   * - Group
     - Dataset
     - Meaning
     - Size
   * - ``gas_grid``
     - ``radial_grid``
     - Cell-face radii defining the radial grid
     - 1000
   * - ``gas_grid``
     - ``surface_density``
     - Gas surface density, \(\Sigma_{\rm g}\)
     - 1000
   * - ``gas_grid``
     - ``radial_velocity``
     - Gas radial velocity, \(v_{r,g}\)
     - 1000
   * - ``gas_grid``
     - ``pressure``
     - Midplane gas pressure, \(P\)
     - 1000
   * - ``gas_grid``
     - ``pressure_gradient``
     - Radial pressure gradient, \(\partial P/\partial r\)
     - 1000
   * - ``dust_grid``
     - ``surface_density``
     - Dust surface density, \(\Sigma_{\rm d}\), mapped onto the radial grid
     - 1000
   * - ``particles``
     - ``index``
     - Particle identifiers
     - 5000
   * - ``particles``
     - ``position``
     - Particle radial positions
     - 5000
   * - ``particles``
     - ``size``
     - Particle sizes
     - 5000
   * - ``frame``
     - ``time``
     - Physical simulation time of the snapshot
     - 1

The file is organized into four top-level groups: ``gas_grid``, ``dust_grid``, ``particles``, and ``frame``.

**Gas grid.** The ``gas_grid`` group contains gas-related fields. The ``radial_grid`` dataset stores the cell-face radii, while the other gas datasets are defined at cell centers:

* ``surface_density`` — gas surface density, \(\Sigma_{\rm g}\);
* ``radial_velocity`` — gas radial velocity, \(v_{r,g}\);
* ``pressure`` — midplane gas pressure, \(P\);
* ``pressure_gradient`` — radial pressure gradient, \(\partial P/\partial r\).

**Dust grid.** When dust evolution is enabled, the ``dust_grid`` group contains the dust surface density profile, \(\Sigma_{\rm d}\), mapped onto the same radial grid.

**Particles.** When dust particles are active, the ``particles`` group stores their properties:

* ``index`` — particle identifiers;
* ``position`` — radial positions;
* ``size`` — particle sizes.

**Frame metadata.** The ``frame`` group contains snapshot-level metadata, including ``time``, the physical simulation time represented by the snapshot.

HDF5 files can be inspected from the terminal using ``h5ls`` or ``h5dump``:

.. code-block:: console

   $ h5ls -r snapshot_00000000.h5
   $ h5dump -d gas_grid/surface_density snapshot_00000000.h5

Snapshots can also be read and analyzed using ``h5py``:

.. code-block:: python

   import h5py

   with h5py.File("snapshot_00000000.h5", "r") as f:
       print(f["gas_grid/surface_density"][:10])

If dust evolution is enabled in a disk with an embedded dead zone, RAPID may also produce the diagnostic file ``mass_accumulation_dze_edge.h5`` in the ``LOGS/`` directory. This file stores the time evolution of pressure-trap properties in the ``trap_evolution`` group. Its datasets include ``primary_mass``, ``secondary_mass``, ``total_mass``, ``trap_position``, and ``time``. They track the accumulated masses of the primary and secondary dust populations at the pressure-trap location, along with the trap position and simulation time. The extendable datasets are updated at each snapshot output, so their entries correspond to the simulation times at which snapshots are written.