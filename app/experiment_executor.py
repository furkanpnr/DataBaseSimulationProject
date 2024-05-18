from config import *
from modules.simulation.service.simulation import Simulation
import json

from rich import print

class ExperimentExecutor:

    def __init__(self, experiments_path: str) -> None:
        self.experiments_path = experiments_path
        self._experiment_idx = 0
        self._total_experiments = 0
        self._read_experiments()

    def execute(self):
        print(f"[bold green]Starting experiments (Total Experiments: {self._total_experiments})\n")
        
        while self._experiment_idx < self._total_experiments:
            print(f"[bold cyan] Experiment ({self._experiment_idx}/{self._total_experiments})\n")
            
            experiment = self._get_experiment()
            
            if experiment is None:
                break
            
            # Execute the experiment
            result = Simulation.execute_experiment(experiment)
            
            # Write the results to the experiment file
            self._write_result_to_experiment(result)

        print("[bold green]All experiments are finished\n")
        print("[bold cyan]See the results in the experiment files\n")
             
    

    def _get_experiment(self):
        with open(self.experiments_path, "r") as f:
            experiments = json.load(f)
        
        experiments = experiments.get("experiments", None)
        
        if experiments is None or len(experiments) == 0:
            raise Exception("No experiments found!")
        
        if self._experiment_idx > len(experiments):
            return None

        experiment = experiments[self._experiment_idx]
        self._experiment_idx += 1
        return experiment
    
    def _read_experiments(self):

        with open(self.experiments_path, "r") as f:
            experiments = json.load(f)
        
        experiments = experiments.get("experiments", None)

        if experiments is None or len(experiments) == 0:
            return
        
        self._total_experiments = len(experiments)

    def _write_result_to_experiment(self, result: dict):
        with open(self.experiments_path, "r") as f:
            experiments_dict = json.load(f)
        
        experiments = experiments_dict.get("experiments", None)

        if experiments is None or len(experiments) == 0:
            raise Exception("No experiments found to write the result!")
        
        experiments[self._experiment_idx - 1]["result"] = result

        with open(self.experiments_path, "w") as f:
            json.dump(experiments_dict, f, indent=4)
