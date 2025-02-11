# ChatGPT-4o conversation
# https://chatgpt.com/share/67ab4351-ec90-8008-b90a-ab7cac2dc5f2

import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

class Cell:
    def __init__(self, id, state, transition_function, energy):
        self.id = id
        self.state = state  # External state
        self.transition_function = transition_function  # Internal function
        self.energy = energy
        self.neighbors = []
        self.prev_state = state  # Track previous state for entropy calculation

    def query_neighbor(self, neighbor):
        """Extract energy from a neighbor based on state difference."""
        difference = np.abs(self.state - neighbor.state)  # Information difference
        energy_transfer = difference  # Directly proportional
        self.energy += energy_transfer
        neighbor.energy -= energy_transfer
        return energy_transfer

    def update_state(self):
        """Update the cell's state using its transition function."""
        self.prev_state = self.state  # Store previous state for entropy tracking
        self.state = self.transition_function(self.state)

    def mutate_transition_function(self):
        """Modify transition function slightly to explore adaptability."""
        if random.random() < 0.1:  # Small chance to mutate
            self.transition_function = lambda x: (x + random.uniform(-1, 1)) % 1

    def entropy_decay(self):
        """Measure entropy decay rate as state stability over time."""
        return np.abs(self.state - self.prev_state)  # Change in state as proxy for entropy

class CellularAutomaton:
    def __init__(self, num_cells):
        self.graph = nx.Graph()
        for i in range(num_cells):
            state = random.uniform(0, 1)
            energy = random.uniform(5, 10)
            transition_function = lambda x: (x + 0.1) % 1  # Simple transition rule
            cell = Cell(i, state, transition_function, energy)
            self.graph.add_node(i, cell=cell)
        
        # Connect cells randomly
        for i in range(num_cells):
            for j in range(i + 1, num_cells):
                if random.random() < 0.2:  # Sparse connection
                    self.graph.add_edge(i, j)
                    self.graph.nodes[i]['cell'].neighbors.append(self.graph.nodes[j]['cell'])
                    self.graph.nodes[j]['cell'].neighbors.append(self.graph.nodes[i]['cell'])
    
    def step(self):
        """Perform one timestep across all cells."""
        for _, data in self.graph.nodes(data=True):
            cell = data['cell']
            if cell.neighbors:
                neighbor = random.choice(cell.neighbors)
                cell.query_neighbor(neighbor)
            cell.update_state()
            cell.mutate_transition_function()
    
    def measure_entropy_decay(self):
        """Compute the average entropy decay across all non-agent cells."""
        entropy_rates = [data['cell'].entropy_decay() for _, data in self.graph.nodes(data=True)]
        return np.mean(entropy_rates)

class Agent:
    def __init__(self, cell):
        self.cell = cell  # The agent is represented by a specific cell
        self.entropy_decay_history = []

    def intelligent_query(self):
        """Choose the best neighbor to extract energy from."""
        if not self.cell.neighbors:
            return
        
        best_neighbor = max(self.cell.neighbors, key=lambda n: np.abs(self.cell.state - n.state))
        self.cell.query_neighbor(best_neighbor)
    
    def adapt(self):
        """Modify transition function to maintain low entropy."""
        self.cell.transition_function = lambda x: (x + 0.05) % 1  # Favor stability
    
    def track_entropy_decay(self):
        self.entropy_decay_history.append(self.cell.entropy_decay())

# Initialize and run the system
num_steps = 50
ca = CellularAutomaton(num_cells=20)
agent = Agent(random.choice(list(ca.graph.nodes(data=True)))[1]['cell'])

environment_entropy_history = []
agent_entropy_history = []

for _ in range(num_steps):
    agent.intelligent_query()
    agent.adapt()
    ca.step()
    agent.track_entropy_decay()
    environment_entropy_history.append(ca.measure_entropy_decay())
    agent_entropy_history.append(agent.cell.entropy_decay())

# Plot entropy decay rates
plt.plot(range(num_steps), environment_entropy_history, label="Environment Entropy Decay")
plt.plot(range(num_steps), agent_entropy_history, label="Agent Entropy Decay", linestyle='dashed')
plt.xlabel("Time Steps")
plt.ylabel("Entropy Decay Rate")
plt.legend()
plt.title("Entropy Decay Rate: Agent vs Environment")
plt.show()
