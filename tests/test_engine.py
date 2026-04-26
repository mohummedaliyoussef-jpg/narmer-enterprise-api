import pytest
import numpy as np
from app.engine import PharaohEngine, DIMS

class TestPharaohEngine:
    def setup_method(self):
        self.engine = PharaohEngine()
        self.inputs = {d: 75 for d in self.engine.dims}

    def test_v_score_range(self):
        score = self.engine.v_score(self.inputs)
        assert 0 <= score <= 100

    def test_v_score_zero_input(self):
        inputs = {d: 0 for d in self.engine.dims}
        score = self.engine.v_score(inputs)
        assert score > 0

    def test_monte_carlo_output(self):
        mc = self.engine.monte_carlo(self.inputs, iterations=500)
        assert "ci_low" in mc
        assert "ci_high" in mc
        assert mc["ci_low"] < mc["ci_high"]

    def test_sensitivity_analysis(self):
        result = self.engine.sensitivity_analysis(self.inputs)
        assert len(result) == len(DIMS)
        assert all(abs(v) >= 0 for v in result.values())
