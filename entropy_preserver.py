import networkx as nx
import numpy as np
import random

class Cell:
    def __init__(self, id, state, transition_function, energy):
        self.id = id
        self.state = state  # External state
        self.transition_function = transition_function  # Internal function
        self.energy = energy
        self.neighbors = []

    def query_neighbor(self, neighbor):
        """Extract energy from a neighbor based on state difference."""
        difference = np.abs(self.state - neighbor.state)  # Information difference
        energy_transfer = difference  # Directly proportional
        self.energy += energy_transfer
        neighbor.energy -= energy_transfer
        return energy_transfer

    def update_state(self):
        """Update the cell's state using its transition function."""
        self.state = self.transition_function(self.state)

    def mutate_transition_function(self):
        """Modify transition function slightly to explore adaptability."""
        if random.random() < 0.1:  # Small chance to mutate
            self.transition_function = lambda x: (x + random.uniform(-1, 1)) % 1

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

class Agent:
    def __init__(self, cell):
        self.cell = cell  # The agent is represented by a specific cell

    def intelligent_query(self):
        """Choose the best neighbor to extract energy from."""
        if not self.cell.neighbors:
            return
        
        best_neighbor = max(self.cell.neighbors, key=lambda n: np.abs(self.cell.state - n.state))
        self.cell.query_neighbor(best_neighbor)
    
    def adapt(self):
        """Modify transition function to maintain low entropy."""
        self.cell.transition_function = lambda x: (x + 0.05) % 1  # Favor stability

# Initialize and run the system
ca = CellularAutomaton(num_cells=10)
agent = Agent(random.choice(list(ca.graph.nodes(data=True)))[1]['cell'])

for _ in range(10):
    agent.intelligent_query()
    agent.adapt()
    ca.step()
