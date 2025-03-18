from fsrs import Rating
from enum import Enum


class RatingEnum(Enum):
    AGAIN = ["Again", Rating.Again]
    EASY = ["Easy", Rating.Easy]
    MEDIUM = ["Medium", Rating.Good]  # 'Good' is the closest to 'Medium' in FSRS
    HARD = ["Hard", Rating.Hard]
    
    
    