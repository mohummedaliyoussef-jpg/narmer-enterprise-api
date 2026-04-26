"""محرك نارمر الإحصائي المتقدم"""
import numpy as np
import multiprocessing as mp
from typing import Dict, List
from app.models import SovereignDimensions

DIMS = SovereignDimensions.get_all()

class PharaohEngine:
    def __init__(self, weights: np.ndarray = None):
        if weights is None:
            weights = np.array([0.085,0.11,0.13,0.09,0.08,0.07,0.085,0.10,0.06,0.065,0.05,0.055,0.04,0.035,0.06,0.03,0.045])
            weights /= weights.sum()
        self.weights = weights
        self.dims = DIMS

    def v_score(self, inputs: Dict[str, float]) -> float:
        vals = np.clip([inputs.get(d, 50)/100.0 for d in self.dims], 0.01, 1.0)
        return float(np.exp(np.sum(self.weights * np.log(vals))) * 100)
    
    # ... (باقي الدوال: monte_carlo, mcmc_parallel, sensitivity_analysis, multi_objective_optimizer)