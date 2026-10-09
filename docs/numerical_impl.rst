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



Mapping Discrete Dust Particles to a Radial Surface Density Field
---------------------------------------------------------------

In ``RAPID``, the dust component is represented by discrete particles carrying masses :math:`m_k` and positions :math:`r_k`. However, gas–dust interaction terms, growth rates, and drift velocities require a continuous dust surface density field :math:`\Sigma_{\mathrm{d}}(r)` defined on the Eulerian grid.

The dust surface density in cell :math:`i` is defined as

.. math::
   :label: dust_surface_density_mapping

   \Sigma_{\mathrm{d}}(r_i)=\frac{M_i}{A_i},

where :math:`M_i` is the total dust mass assigned to cell :math:`i`, and :math:`A_i=2\pi r_i\Delta r` is the area of the corresponding annulus.

The routine ``calculateDustSurfaceDensity`` provides four mapping and smoothing schemes:

.. figure:: fig_06.png
   :align: center
   :width: 100%

   Comparison of the four mapping and smoothing modes (NGP, CIC, TopHat, and Gaussian) across three test profiles: a steep jump modeling a snowline (left), a pulse train illustrating discrete sampling (middle), and a narrow density pile-up at a pressure maximum (right). Insets highlight the local behavior of each method near sharp gradients.

1. **Nearest Grid Point (NGP)**

   The NGP method assigns the entire mass of each particle to the nearest grid cell. The mass contribution to cell :math:`i` is

   .. math::
      :label: ngp_mapping

      \begin{aligned}
      M_i &= \sum_k m_k W_{\mathrm{NGP}}(r_k-r_i),\\
      W_{\mathrm{NGP}}(x) &=
      \begin{cases}
      1, & |x|<\frac{\Delta r_i}{2},\\
      0, & \text{otherwise}.
      \end{cases}
      \end{aligned}

   NGP preserves sharp peaks and particle locations, but is sensitive to sparse sampling and can introduce substantial numerical shot noise.

2. **Cloud-in-Cell (CIC)**

   CIC distributes the mass of each particle linearly between the two grid points that bracket its position. Define the fractional grid coordinate

   .. math::

      \xi=\frac{r_k-r_{\min}}{\Delta r_i},
      \qquad i=\lfloor\xi\rfloor,

   and let :math:`x=\xi-i`. The mass contributions are then

   .. math::
      :label: cic_mapping

      \begin{aligned}
      M_i &\mathrel{+}=m_k(1-x),\\
      M_{i+1} &\mathrel{+}=m_kx.
      \end{aligned}

   CIC reduces numerical noise and produces smoother profiles than NGP, although it broadens sharp features.

3. **Top-Hat Smoothing**

   Applied *after* the initial CIC mapping, top-hat smoothing replaces each cell value with a three-point moving average over adjacent cells:

   .. math::
      :label: tophat_smoothing

      \Sigma_{\mathrm{d}}^{\mathrm{TH}}(r_i)
      =
      \frac{1}{3}
      \left[
      \Sigma_{\mathrm{d}}(r_{i-1})
      +\Sigma_{\mathrm{d}}(r_i)
      +\Sigma_{\mathrm{d}}(r_{i+1})
      \right].

   This suppresses high-frequency shot noise while retaining the overall shape of the dust distribution and the sharpness of concentration peaks.

4. **Gaussian Smoothing**

   Gaussian smoothing convolves the mapped mass field with a parameterized Gaussian kernel:

   .. math::
      :label: gaussian_kernel

      W(r)=
      \exp\left[-\frac{(r-r_i)^2}{2\sigma^2}\right],
      \qquad
      \sigma=\sigma_{\mathrm{grid}}\Delta r_i.

   The kernel is truncated beyond a user-specified cutoff, where :math:`|r-r_i|>\mathrm{cutoff}\,\sigma`. The smoothed surface density at :math:`r_i` is calculated as

   .. math::
      :label: gaussian_smoothing

      \Sigma_{\mathrm{d}}^{\mathrm{G}}(r_i)
      =
      \frac{
      \displaystyle\sum_{j=i-N}^{i+N}
      \Sigma_{\mathrm{d}}(r_j)
      \exp\left[-\frac{(r_j-r_i)^2}{2\sigma^2}\right]
      }{
      \displaystyle\sum_{j=i-N}^{i+N}
      \exp\left[-\frac{(r_j-r_i)^2}{2\sigma^2}\right]
      },

   where the cutoff is applied according to the physical distance from the kernel center. This method provides controlled smoothing while retaining narrow structures.

To illustrate the numerical behavior and dissipation characteristics of these algorithms, the methods were tested on three artificial density profiles. The left panel of :numref:`fig:smoothingalgs` shows a steep surface-density jump, representative of a planetary snowline where volatile species condense or evaporate. This profile tests the ability of each method to preserve sharp boundaries without excessive numerical diffusion.

The middle panel shows a pulse train that illustrates sampling artifacts. As particles drift across the grid towards the central star, the discrete mapping can leave some Eulerian cells unpopulated while neighbouring cells accumulate multiple particles, resulting in substantial shot noise.

The right panel shows a narrow Gaussian density peak, representing dust accumulation near a local pressure maximum. This profile demonstrates how effectively each method preserves narrow spatial structures.

The choice of mapping and smoothing scheme depends on the purpose of the simulation. Top-hat and Gaussian smoothing can fill gaps in the mapped dust surface density, but may artificially broaden sharp features and dampen density peaks. In contrast, unsmoothed NGP and CIC preserve sharper transitions and local extrema, but can retain the uneven peaks and gaps associated with sparse particle sampling.

Field-Dependent Boundary Condition Approach
-------------------------------------------

.. figure:: fig_07.png
   :align: center
   :width: 90%

   Evolution of the gas surface density (:math:`\Sigma`, left panels) and gas radial velocity (:math:`v_{\mathrm{g}}`, right panels) from :math:`t=0` to :math:`30\,\mathrm{kyr}` for boundary condition types 0–4. The initial state follows a power-law surface-density profile with a localized Gaussian perturbation centered at :math:`r=1.8`. The initial velocity field is derived from these conditions. Vertical dotted red lines mark the physical disk boundaries, :math:`r_{\min}=1.0` and :math:`r_{\max}=3.0`, and indicate the neighbouring ghost cells. All simulations use a linear grid.

Applying the explicit finite-difference scheme to the calculated fields—including the gas surface density :math:`\Sigma_{\mathrm{g}}`, pressure :math:`P`, pressure gradient :math:`\partial P/\partial r`, and gas radial velocity :math:`v_{\mathrm{r,g}}`—requires updating the ghost cells at the inner and outer grid boundaries. The ghost-cell indices are :math:`i=0` and :math:`i=N_{\mathrm{grid}}+1`, respectively.

Some boundary conditions are formulated specifically for mass transport and gas surface density. Applying them directly to pressure or pressure-gradient fields can introduce non-physical artifacts and numerical instabilities. To avoid this, ``RAPID`` uses a field-dependent correction layer that redirects incompatible boundary conditions to fallback operators. For example, absorbing conditions are replaced by zero-gradient conditions, while fixed-flux conditions fall back to second-order parabolic extrapolation for secondary fields such as pressure and its gradient.

The routine ``applyBoundaryConditions`` applies the selected boundary operator independently to each field :math:`q` at each grid boundary.

**Zero-Gradient (Type 0)**

The zero-gradient condition copies the value of the nearest interior cell into the ghost cell:

.. math::
   :label: bc_zero_gradient

   q_0=q_1,
   \qquad
   q_{N+1}=q_N.

This condition is simple and robust, but can act as a reflective barrier and induce artificial accumulation or local extrema in the gas and dust distributions.

**Parabolic Extrapolation (Type 1)**

Parabolic extrapolation fits a quadratic polynomial through three reference points to provide second-order extrapolation at the boundary. The polynomial is

.. math::
   :label: bc_parabola

   q(x)=ax^2+bx+c.

Given three reference coordinates :math:`x_1`, :math:`x_2`, and :math:`x_3`, with corresponding field values :math:`q_1`, :math:`q_2`, and :math:`q_3`, the coefficients are

.. math::
   :label: bc_parabola_coefficients

   \begin{aligned}
   a &=
   \frac{
   \displaystyle\frac{q_1-q_3}{x_1-x_3}
   -
   \displaystyle\frac{q_1-q_2}{x_1-x_2}
   }{x_3-x_2},\\
   b &=
   \frac{q_1-q_2}{x_1-x_2}-a(x_1+x_2),\\
   c &=q_1-ax_1^2-bx_1.
   \end{aligned}

The ghost-cell value is evaluated at the corresponding ghost coordinate, :math:`x_{\mathrm{ghost}}=r_{\min}-\Delta r` at the inner boundary or :math:`x_{\mathrm{ghost}}=r_{\max}+\Delta r` at the outer boundary:

.. math::
   :label: bc_parabola_ghost

   q_{\mathrm{ghost}}
   =
   ax_{\mathrm{ghost}}^2
   +bx_{\mathrm{ghost}}+c.

This condition provides smooth higher-order extrapolation, although it can produce overshoots or oscillations when sharp gradients approach a boundary.

**Fixed-Flux (Type 2)**

The fixed-flux condition imposes a viscous mass flux based on the prescription of Lynden-Bell and Pringle (1974). At the inner boundary,

.. math::
   :label: bc_fixed_flux

   q_0=q_1\sqrt{\frac{r_1}{r_0}},

while the outer boundary uses a stable outflow condition:

.. math::

   q_{N+1}=q_N.

Although designed for accretion disks, this condition assumes a steady-state viscous transport profile and may be less suitable during rapidly evolving phases.

**Absorbing (Type 3)**

The absorbing condition sets the ghost-cell values to zero:

.. math::
   :label: bc_absorbing

   q_0=0,
   \qquad
   q_{N+1}=0.

This acts as a sink that removes material from the computational domain. However, it can also generate steep, unphysical gradients and inward-propagating pressure waves. When the inner boundary is close to the central star, this behavior can approximate free accretion onto the stellar surface.

**Reflecting (Type 4)**

The reflecting condition mirrors the field symmetrically across the active boundaries:

.. math::
   :label: bc_reflecting

   q_0=q_2,
   \qquad
   q_{N+1}=q_{N-1}.

This condition prevents flux through the boundaries, but also reflects waves back into the computational domain.

Figures :numref:`fig:sigma_vg_evolution` and :numref:`fig:pressure_dpdr_evolution` show the evolution of a fiducial disk over :math:`30\,\mathrm{kyr}` for all five boundary condition types. The initial surface-density profile follows a power law (see :eq:`sigmapower`) with a localized Gaussian perturbation centered at :math:`r=1.8\,\mathrm{AU}`. The grid extends from :math:`1.0` to :math:`3.0\,\mathrm{AU}` and contains 100 equidistant cells.