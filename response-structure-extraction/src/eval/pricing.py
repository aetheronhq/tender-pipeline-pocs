"""Centralized pricing logic for Gemini models."""
from typing import Dict, Tuple

# Pricing rates per 1M tokens (USD)
# Source: Gemini API Pricing (Dec 2025)
PRICING_TABLE = {
    # Workhorse model
    "gemini-2.5-flash": {
        "input": 0.15,
        "output": 0.60,
        "input_cached": 0.04
    },
    # Reasoning model (standard < 128k context)
    "gemini-1.5-pro": {
        "input": 3.50,
        "output": 10.50,
        "input_cached": 0.875
    },
    # Flagship model (standard < 200k context)
    "gemini-3.0-pro": {
        "input": 2.00,
        "output": 12.00
    },
    # Flagship model (long context > 200k)
    "gemini-3.0-pro-long": {
        "input": 4.00,
        "output": 18.00
    }
}

def calculate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """Calculate USD cost based on token usage and model type."""
    model_key = model.lower()
    
    # Handle long context logic for 3.0 Pro
    if "gemini-3.0-pro" in model_key and input_tokens > 200_000:
        model_key = "gemini-3.0-pro-long"
    # Fallback/Normalization
    elif "flash" in model_key:
        model_key = "gemini-2.5-flash"
    elif "pro" in model_key and "3.0" not in model_key:
        model_key = "gemini-1.5-pro" # Fallback for older Pro calls

    rates = PRICING_TABLE.get(model_key, PRICING_TABLE["gemini-2.5-flash"])
    
    cost_input = (input_tokens / 1_000_000) * rates["input"]
    cost_output = (output_tokens / 1_000_000) * rates["output"]
    
    return round(cost_input + cost_output, 6)
