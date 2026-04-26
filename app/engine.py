import numpy as np
from typing import Dict, List, Optional

DIMS = [
    "الحوكمة والامتثال", "القوة العسكرية", "المناعة السيبرانية",
    "الاقتصاد الرقمي", "الأمن الغذائي", "أمن الطاقة",
    "الاستقرار السياسي", "الأمن الصحي", "التعليم والتدريب",
    "البنية التحتية", "الموارد المائية", "الغطاء النباتي",
    "إدارة الكوارث", "الابتكار والتقنية", "النفوذ الدبلوماسي",
    "تماسك المجتمع", "العدالة وسيادة القانون"
]

class PharaohEngine:
    def __init__(self, weights: Optional[np.ndarray] = None):
        if weights is None:
            weights = np.array([0.085, 0.11, 0.13, 0.09, 0.08, 0.07, 0.085, 0.10, 0.06, 0.065, 0.05, 0.055, 0.04, 0.035, 0.06, 0.03, 0.045])
            weights = weights / weights.sum()
        self.weights = weights
        self.dims = DIMS

    def v_score(self, inputs: Dict[str, float]) -> float:
        vals = np.clip([inputs.get(d, 50)/100.0 for d in self.dims], 0.01, 1.0)
        return float(np.exp(np.sum(self.weights * np.log(vals))) * 100)

    def monte_carlo(self, inputs: Dict[str, float], iterations: int = 1000) -> Dict:
        base_vals = np.array([inputs.get(d, 50) for d in self.dims])
        samples = np.random.normal(base_vals, 5.0, (iterations, len(self.dims)))
        scores = np.exp(np.sum(self.weights * np.log(np.clip(samples/100.0, 0.01, 1.0)), axis=1)) * 100
        ci_low = float(np.percentile(scores, 2.5))
        ci_high = float(np.percentile(scores, 97.5))
        risk = float(np.mean(scores < 50))
        return {"ci_low": ci_low, "ci_high": ci_high, "risk": risk, "median": float(np.median(scores))}

    def sensitivity_analysis(self, inputs: Dict[str, float], delta: float = 10.0) -> Dict:
        base_score = self.v_score(inputs)
        impacts = {}
        for d in self.dims:
            perturbed = inputs.copy()
            perturbed[d] = min(100, perturbed.get(d, 50) + delta)
            impacts[d] = self.v_score(perturbed) - base_score
        return dict(sorted(impacts.items(), key=lambda x: abs(x[1]), reverse=True))
