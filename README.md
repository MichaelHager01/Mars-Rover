# Mars rover

A four-phase simulation of a rover landing on Mars and driving to a point on the surface.

## What it does

- Phase 1 models mass, gear ratio, motor torque, gravity, rolling resistance, and net force, then plots how speed changes with terrain and rover properties.
- Phase 2 runs a driving experiment with SciPy interpolation and `solve_ivp`.
- Phase 3 models the entry, descent, and landing system, including Mach-dependent parachute drag. It imports `define_edl_system`, `define_planet`, and `define_mission_events`, and those modules are not in this repository.
- Phase 4 searches a five-variable landing and rover design with SciPy's constrained optimizer for the class design competition.
- The original function-by-function notes are in `docs/phase-notes.md`.

## Layout

- `src/phase1/` — rover forces and the first plots
- `src/phase2/` — driving experiment
- `src/phase3/` — entry, descent, and landing
- `src/phase4/` — design optimization
- `docs/phase-notes.md` — the original phase writeup

## Run

From the repository root:

```bash
pip install -r requirements.txt
python src/phase1/analysis_terrain_slope.py
python src/phase2/rover_experiment1.py
```

Run a phase file from its own directory if an import of a sibling module fails. Phase 3 needs the three missing definition modules beside `src/phase3/` before it can run. Contributors: Elizabeth and Savera.

## Stack

Python, NumPy, SciPy, Matplotlib. Written for the Texas A&M engineering analysis course.
