
from typing import Any, Dict, Iterable, List


def generate_recommendations(predictions: Iterable[float], metrics: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Generate business recommendations based on forecast metrics.

    Parameters:
        predictions: Forecasted sales values.
        metrics: Dictionary containing percentage change metrics.

    Returns:
        List of recommendation dictionaries with title, description, and expected impact.
    """
    recommendations: List[Dict[str, str]] = []

    increase_pct = metrics.get("percent_change_vs_last_day", 0)

    if increase_pct < -20:
        recommendations.append(
            {
                "title": "Increase promotions",
                "description": "Consider offering a targeted 10–15% discount to stimulate demand "
                               "and recover from a significant forecasted decline.",
                "expected_impact": "10-15% improvement in conversion and order volume",
            }
        )
        recommendations.append(
            {
                "title": "Increase marketing spend",
                "description": "Boost social media advertising and awareness campaigns to attract "
                               "new customers and offset the downward trend.",
                "expected_impact": "8-12% increase in traffic and qualified leads",
            }
        )
        recommendations.append(
            {
                "title": "Reduce inventory risk",
                "description": "Limit new stock commitments and manage inventory closely to avoid "
                               "excess holdings during the forecasted decline.",
                "expected_impact": "Lower carrying costs and reduced stock write-offs",
            }
        )
    elif increase_pct > 10:
        recommendations.append(
            {
                "title": "Increase inventory",
                "description": "Prepare for rising demand by increasing inventory levels "
                               "for high-performing products.",
                "expected_impact": "Improved fulfillment rates and reduced stockouts",
            }
        )
        recommendations.append(
            {
                "title": "Expand marketing",
                "description": "Scale marketing efforts to capture additional demand and support "
                               "the positive sales trend.",
                "expected_impact": "10-15% uplift in lead generation and brand visibility",
            }
        )
    else:
        recommendations.append(
            {
                "title": "Maintain current strategy",
                "description": "Monitor performance closely while keeping the current sales "
                               "and marketing plan in place.",
                "expected_impact": "Stable operations with low risk of overreaction",
            }
        )

    return recommendations


def generate_insights(metrics: Dict[str, Any]) -> str:
    """
    Generate a short insight text based on forecast metrics.

    Parameters:
        metrics: Dictionary containing percentage change metrics.

    Returns:
        Short business-oriented insight about the trend.
    """
    change = metrics.get("percent_change_vs_last_day", 0)

    if change < -20:
        return "Forecast shows a sharp decline; prioritize demand stimulation and cost control."
    if change > 10:
        return "Forecast indicates strong sales growth; focus on scaling supply and marketing."
    return "Forecast is stable; continue current operations and monitor performance."
