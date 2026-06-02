"""
Protein food factories.
"""

from .meat import create_beef, create_chicken
from .fish import create_salmon
from .eggs import create_egg
from .legumes import create_lentils
from .plant import create_tofu

__all__ = [
    "create_beef",
    "create_chicken", 
    "create_salmon",
    "create_egg",
    "create_lentils",
    "create_tofu",
]
