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
-------------------------

Both the Python wrapper in the source repository and the installed `rapidsim` package use the same YAML-based configuration format. The configuration file organises simulation settings into sections for the physical processes, disk properties, boundary conditions, dust parameters, output, time integration, and logging.

Create a file named `config.yaml` and specify the parameters for the desired simulation.

**[Insert YAML configuration example here]**

For a complete description of the available configuration parameters and their default values, see the [configuration documentation](INSERT-CONFIGURATION-DOCUMENTATION-URL).

5. Output and further documentation
-----------------------------------

After a simulation finishes, RAPID writes the results to the output directory specified in the configuration file. Depending on the selected output format, the simulation snapshots are stored as ASCII text files or HDF5 files. Diagnostic and runtime information is also generated.

For more information about the simulation parameters, output files, example configurations, and benchmark tests, consult the [RAPID documentation](https://rapiddocs.readthedocs.io/en/latest/).