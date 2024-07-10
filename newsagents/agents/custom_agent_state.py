from enum import Enum
from genworlds.agents.abstracts.agent_state import AbstractAgentState
from newsagents.agents.thoughts.agent_bulider import AgentBuilder
from newsagents.world.world_map import NewsCategory
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

def create_agent_states(agents: List[AgentBuilder]) -> List[CustomAgentState]:
    return [
        CustomAgentState(
            id=agent.id,
            name=agent.name,
            description=agent.description,
            host_world_prompt=agent.host_world_prompt,
            simulation_memory_persistent_path="newsworld/newsagents/agents/memories",
            memory_ignored_event_types=set(),
            wakeup_event_types=[],
            action_schema_chains=[],
            goals=[
                "According to the group you belong to and the characteristics of the group, capture the different views and reactions of students from different backgrounds, titles, and majors to news events.",
                "Participate in discussions and debates on current affairs and express your attitudes and emotions towards news reports.",
                "According to the group's emotions and attitudes, take interactive actions such as sharing, commenting, liking, and following related news content."
            ],
            plan=[],
            last_retrieved_memory="",
            other_thoughts_filled_parameters={},
            available_action_schemas={
            },
            available_entities=[],
            is_asleep=False,
            current_action_chain=[],
            emotion={"happiness": 0.0, "sadness": 0.0, "anger": 0.0},
            attitude={"optimism": 0.0, "pessimism": 0.0, "neutrality": 0.0},
            population_category=PopulationCategory.SUSCEPTIBLE,
            news_content=[]
        ) for agent in agents
    ]