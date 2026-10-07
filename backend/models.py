# Data models for user requirements, product evaluation, and API requests.

from pydantic import BaseModel, Field
from typing import List, Optional


class UserRequirements(BaseModel):

    budget: Optional[float] = Field(
        description="Maximum budget in EGP"
    )

    usage: List[str] = Field(
        description="Main purposes for using the laptop"
    )

    min_ram: Optional[int] = Field(
        description="Minimum required RAM in GB"
    )

    priorities: List[str] = Field(
        description="Features that are important to the user"
    )


class ProductEvaluation(BaseModel):

    product: str
    budget_match: str
    ram_match: str
    gaming_suitability: str


class RecommendationRequest(BaseModel):

    user_text: str
    urls: List[str]