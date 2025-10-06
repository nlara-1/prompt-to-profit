# scoring.py
from typing import Dict

def interpret_kpis(delta: Dict[str, int], priority: str, weights: Dict[str, float]) -> str:
    """Explain KPI results relative to priorities."""
    insights = []
    for k, v in delta.items():
        w = weights.get(k, 1.0)
        adj = v * w
        if k == priority:
            if adj > 4:
                insights.append(f"excellent focus on {k}")
            elif adj > 2:
                insights.append(f"strong emphasis on {k}")
            elif adj > 0:
                insights.append(f"some progress on {k}")
        else:
            if adj > 4:
                insights.append(f"high {k} gains but off-priority")
            elif adj > 2:
                insights.append(f"steady {k}")
            elif adj < 0:
                insights.append(f"weaker {k}")
    return ", ".join(insights) if insights else "balanced but neutral results."
