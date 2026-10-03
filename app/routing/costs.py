from app.constants import CIRCUITY, WALK_SPEED_MPS

def walk_s(meters: float) -> float:
    return meters * CIRCUITY / WALK_SPEED_MPS
