from typing import TypedDict, List

class TripState(TypedDict, total=False):
    user_input: str
    persona: List[str]
    destination_scores: dict
    destinations: List[str]
    top_destination: str
    itinerary: str
    culture_tips: str
    packing_list: str