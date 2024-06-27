from enum import Enum
from genworlds.agents.abstracts.agent_state import AbstractAgentState
from pydantic import Field
from typing import Dict, List

class PopulationCategory(str, Enum):
    SUSCEPTIBLE = "Susceptible Population"
    AVERAGE = "Average Population"
    CALM = "Calm Population"

    def get_description(self):
        descriptions = {
            PopulationCategory.SUSCEPTIBLE: (
                "This category of individuals tends to be easily influenced by news reports, "
                "often experiencing pronounced emotional and attitudinal responses to the content, "
                "and taking different actions accordingly."
            ),
            PopulationCategory.AVERAGE: (
                "This category typically comprises individuals with moderate receptivity to news, "
                "showing a balanced mix of emotional reactions and attitudes towards news events."
            ),
            PopulationCategory.CALM: (
                "Individuals in this category exhibit a composed and measured response to news, "
                "often maintaining a level-headed demeanor regardless of the content, resulting in "
                "relatively stable attitudes towards news."
            )
        }
        return descriptions[self]
    

class CustomAgentState(AbstractAgentState):
    emotion: Dict[str, float] = Field(..., description="Emotional state of the agent.")
    attitude: Dict[str, float] = Field(..., description="Attitude of the agent.")
    population_category: PopulationCategory = Field(..., description="Population category of the agent.")
    # is_planning: bool = Field(..., description="Indicates whether the agent wants to update the plan.")
    news_content: List[str] = Field(..., description="List of strings representing the context of news that the agent is dealing with.")
    news_views: int = Field(0, description="Number of views for the news.")
    news_likes: int = Field(0, description="Number of likes for the news.")
    news_comments: int = Field(0, description="Number of comments for the news.")
    news_shares: int = Field(0, description="Number of shares for the news.")
    news_follows: int = Field(0, description="Number of follows for the news.")
    num_temp: int = Field(0, description="Used to store temporary data.")

    def update_news_views(self, increment: int = 1):
        self.news_views += increment

    def update_news_likes(self, increment: int = 1):
        self.news_likes += increment

    def update_news_comments(self, increment: int = 1):
        self.news_comments += increment

    def update_news_shares(self, increment: int = 1):
        self.news_shares += increment

    def update_news_follows(self, increment: int = 1):
        self.news_follows += increment
