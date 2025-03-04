"""
Entry point for the life simulation.
"""

from src.simulation import Simulation

def main():
    """Initialize and run the simulation."""
    simulation = Simulation()
    simulation.run()

if __name__ == "__main__":
    main() 