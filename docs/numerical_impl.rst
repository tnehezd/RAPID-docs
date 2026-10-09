Numerical Implementation
========================

The numerical implementation of ``RAPID`` solves the 1D hybrid Eulerian–Lagrangian gas and dust evolution equations presented in :ref:`governing_equations`. The code is modular and open source, written in C++ with OpenMP-based multithreading for parallel execution. Individual physical processes are handled by separate routines.

The gas phase is treated as a continuous fluid evolved on a fixed Eulerian grid, using the viscous evolution equation. The dust phase is modeled by integrating the equations of motion of individual Lagrangian particles.

Spatial Discretization and Grid Geometry
----------------------------------------

``RAPID`` supports both equidistant linear and logarithmic radial grids for the gas component. For a linear grid, the radial coordinates of cell centers are defined as

.. math::
   :label: radial_grid

   r_i = r_{\min} + \left(i-\frac{1}{2}\right)\Delta r,

where

.. math::

   \Delta r = \frac{r_{\max}-r_{\min}}{N_{\mathrm{grid}}},

and :math:`N_{\mathrm{grid}}` is the number of physical cells. For a logarithmic grid, the local spacings :math:`\Delta r_i = r_{i+1}-r_i` are used in the finite-difference operators and particle mapping (see :ref:`dust_mapping`).

The gas surface density :math:`\Sigma_{\mathrm{g}}` is updated using an explicit Forward-Time Central-Space (FTCS) finite-difference scheme, which is second-order accurate in space and first-order accurate in time. The viscous evolution equation (see :eq:`gaseq1d`) is formulated in terms of the combined variable

.. math::

   u \equiv \nu\Sigma_{\mathrm{g}},

where :math:`\nu` is the kinematic viscosity. After each update, the physical surface density is recovered as

.. math::

   \Sigma_{\mathrm{g}} = \frac{u}{\nu}.

To formulate the numerical operator, the spatial derivatives are expanded using the product rule. The inner derivative, multiplied by :math:`r^{1/2}`, gives

.. math::

   r\frac{\partial u}{\partial r}+\frac{1}{2}u.

Taking the outer radial derivative yields

.. math::
   :label: expanded_viscous_operator

   \frac{\partial}{\partial r}
   \left(r\frac{\partial u}{\partial r}+\frac{1}{2}u\right)
   =
   r\frac{\partial^2u}{\partial r^2}
   +\frac{3}{2}\frac{\partial u}{\partial r}.

Multiplying by the prefactor :math:`3/r` from the viscous evolution equation gives

.. math::

   \frac{3}{r}
   \left(
   r\frac{\partial^2u}{\partial r^2}
   +\frac{3}{2}\frac{\partial u}{\partial r}
   \right)
   =
   3\frac{\partial^2u}{\partial r^2}
   +\frac{9}{2r}\frac{\partial u}{\partial r}.

For a generic radial cell :math:`i`, the corresponding spatial operator is evaluated using second-order central differences:

.. math::
   :label: discrete_viscous_operator

   \begin{aligned}
   &\left[
   \frac{\partial}{\partial r}
   \left(
   r^{1/2}\frac{\partial}{\partial r}(ur^{1/2})
   \right)
   \right]_i
   \approx {}\\
   &\quad C_{2,i}
   \frac{u_{i+1}-2u_i+u_{i-1}}{\Delta r^2}
   +C_{1,i}
   \frac{u_{i+1}-u_{i-1}}{2\Delta r},
   \end{aligned}

where the coefficients include the local kinematic viscosity:

.. math::

   C_{2,i}=3\nu(r_i), \qquad
   C_{1,i}=\frac{9\nu(r_i)}{2r_i}.

Gas–Particle Coupling and Temporal Integration
----------------------------------------------

The interaction between the gas disk and dust particles is implemented using one-way coupling. Aerodynamic drag from the surrounding gas affects the motion of the dust particles, while the back-reaction of the dust on the gas is neglected in the current version of the code.

The radial positions of the Lagrangian particles are advanced using a fourth-order Runge–Kutta (RK4) scheme. For a particle at position :math:`r_k` with radial drift velocity :math:`v_{\mathrm{r,d}}(r)`, the four intermediate slopes are

.. math::
   :label: rk4_slopes

   \begin{aligned}
   k_1 &= v_{\mathrm{r,d}}(r_k),\\
   k_2 &= v_{\mathrm{r,d}}\left(r_k+\frac{1}{2}\Delta t\,k_1\right),\\
   k_3 &= v_{\mathrm{r,d}}\left(r_k+\frac{1}{2}\Delta t\,k_2\right),\\
   k_4 &= v_{\mathrm{r,d}}\left(r_k+\Delta t\,k_3\right).
   \end{aligned}

The updated particle position is calculated from the weighted average of these slopes:

.. math::
   :label: rk4_update

   r_k^{\mathrm{new}}
   =
   r_k+\frac{\Delta t}{6}
   \left(k_1+2k_2+2k_3+k_4\right).

Local gas properties required at the intermediate stages are interpolated linearly to the particle position. For a particle at :math:`r_k` between two neighbouring grid points, :math:`r_i\leq r_k<r_{i+1}`, a gas property :math:`q` is evaluated as

.. math::
   :label: linear_interpolation

   q(r_k)
   =
   q_i+
   \frac{q_{i+1}-q_i}{r_{i+1}-r_i}(r_k-r_i),

where :math:`q_i` and :math:`q_{i+1}` are the values at the neighbouring grid points.

Because the dust is represented by discrete Lagrangian particles, its spatial distribution can become sparse and uneven. To obtain a continuous dust surface density field :math:`\Sigma_{\mathrm{d}}` for dust-growth calculations, the particle distribution is mapped back onto the Eulerian grid using the methods described in :ref:`dust_mapping`.

Time Integration and Stability Criteria
---------------------------------------

The main integration loop adaptively adjusts the computational time step :math:`\Delta t` to satisfy the stability constraints associated with gas evolution, photoevaporation, and dust transport.

First, the explicit FTCS scheme for viscous gas evolution imposes the following stability constraint:

.. math::
   :label: viscous_timestep

   \Delta t_{\mathrm{visc}}
   =
   \min_i\left[
   C_{\mathrm{visc}}\frac{\Delta r_i^2}{2\nu_i}
   \right],

where :math:`C_{\mathrm{visc}}=0.35` is the viscous safety factor, :math:`\Delta r_i` is the local radial spacing, and :math:`\nu_i` is the local kinematic viscosity. This constraint limits the amount of viscous diffusion occurring during a single time step.

When photoevaporation is enabled, an additional constraint prevents a cell from losing too much of its gas surface density in one step:

.. math::
   :label: photoevap_timestep

   \Delta t_{\mathrm{photo}}
   =
   0.15\min_i
   \left(
   \frac{\Sigma_{\mathrm{g},i}}
   {\dot{\Sigma}_{\mathrm{photo},i}}
   \right).

The movement of the Lagrangian dust particles is also constrained by a Courant–Friedrichs–Lewy (CFL) condition:

.. math::
   :label: dust_timestep

   \Delta t_{\mathrm{dust}}
   =
   C_{\mathrm{dust}}
   \frac{\Delta r}{v_{\mathrm{drift,max}}},

where :math:`C_{\mathrm{dust}}=0.40` is the dust safety factor and :math:`v_{\mathrm{drift,max}}` is computed by ``getMaximumDriftVelocity``.

The new time step is selected as the minimum of the applicable constraints:

.. math::
   :label: new_timestep

   \Delta t_{\mathrm{new}}
   =
   \min\left(
   \Delta t_{\mathrm{visc}},
   \Delta t_{\mathrm{photo}},
   \Delta t_{\mathrm{dust}}
   \right).

To reduce abrupt changes caused by variations in the calculated drift velocity, the code applies temporal smoothing:

.. math::
   :label: timestep_smoothing

   \Delta t^n
   =
   0.7\Delta t^{n-1}
   +0.3\Delta t_{\mathrm{new}}.
