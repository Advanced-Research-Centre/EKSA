# EKSA
Embedded Knowledge Seeking Agent

The agent can move on the grid. Every grid cell is a qubit. It may or may not be entangled with other qubits. The environment does some 'unknown to the agent' unitary computation at every step, e.g., run H or some qubits or run CZ on neighboring qubits. It is not random; the scheme is deterministic and periodic. The agent can measure the cell it is on, or move to another grid, or wait at the current grid. The agent's job is to move around on the grid and figure out the environment's unitary computation scheme. Simulate something like a loophole-free bell pair experiment.
