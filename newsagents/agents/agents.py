import sys
from time import sleep
import traceback
from typing import List, Type, Dict, Any

from genworlds.agents.abstracts.agent import AbstractAgent
from genworlds.events.abstracts.action import AbstractAction
from genworlds.events.abstracts.event import  NewsEvent
from newsagents.agents.custom_state_manager import CustomStateManager
from newsagents.agents.custom_action_planner import CustomActionPlanner
from newsagents.agents.custom_agent_state import CustomAgentState
from newsagents.agents.thoughts.action_schema_selector import ActionSchemaSelectorThought
from newsagents.agents.thoughts.event_filler import EventFillerThought
from genworlds.agents.abstracts.thought import AbstractThought
from genworlds.utils.logging_factory import LoggingFile
from newsagents.events.events import (
    #NewsPropagationAction,
    AgentViewsNewsAndUpdateStateAction,
    AgentLikesNewsAction,
    AgentCommentsOnNewsAction,
    AgentFollowsNewsAction,
    AgentSharesNewsAction
)
from newsagents.world.custom_actions import (
    UpdateAgentAvailableActionSchemas,
    UpdateAgentAvailableEntities
)


class NewsNetworkAgent(AbstractAgent):
    def __init__(
        self,
        openai_api_key: str,
        name: str,
        id: str,
        description: str,
        host_world_prompt: str,
        initial_agent_state: CustomAgentState,
        action_classes: List[type[AbstractAction]] = [],
        other_thoughts: List[AbstractThought] = [],
        model_name: str = "llama3",

    ):

        self.logger = LoggingFile.get_logger(self.__class__.__name__)

        state_manager = CustomStateManager(
            self, initial_agent_state, openai_api_key
        )
        action_planner = CustomActionPlanner(
            openai_api_key=openai_api_key,
            host_agent=self,
            initial_agent_state=state_manager.state,
            other_thoughts=other_thoughts,
            model_name=model_name
        )
        actions = []
        for action_class in action_classes:
            actions.append(action_class(host_object=self))

        actions.append(UpdateAgentAvailableEntities(host_object=self))
        actions.append(UpdateAgentAvailableActionSchemas(host_object=self))
        actions.append(AgentViewsNewsAndUpdateStateAction(host_object=self))
        actions.append(AgentLikesNewsAction(host_object=self))
        actions.append(AgentCommentsOnNewsAction(host_object=self))
        actions.append(AgentFollowsNewsAction(host_object=self))
        actions.append(AgentSharesNewsAction(host_object=self))
        #actions.append(NewsPropagationAction(host_object=self))
        
        super().__init__(name, id, description, state_manager, action_planner, host_world_prompt, actions)

    def add_wakeup_event(self, event_class: NewsEvent):
        self.state_manager.state.wakeup_event_types.add(
            event_class.model_fields["event_type"].default
        )

    def add_memory_ignored_event(self, event_type: str):
        self.state_manager.state.memory_ignored_event_types.add(event_type)


# Function to create agents from agent states
def create_agents_from_states(agent_states: List[CustomAgentState]) -> List[NewsNetworkAgent]:
    action_classes = []  # Define your action classes here if needed
    
    agents = []
    for state in agent_states:
        agent = NewsNetworkAgent(
            openai_api_key="llama3",
            name=state.name,
            id=state.id,
            description=state.description,
            initial_agent_state=state,
            action_classes=action_classes,
            other_thoughts=[],
            host_world_prompt=state.host_world_prompt,
        )
        agents.append(agent)
    
    return agents

    # def add_views(self):
    #     """Increment the views count for the agent and print the updated total."""
    #     self.views += 1
    #     self.logger.info(f"Agent {self.id} has a total of {self.views} views.")
    #     print(f"Agent {self.id} has a total of {self.views} views.")

    # def add_likes(self):
    #     """Increment the likes count for the agent and print the updated total."""
    #     self.likes += 1
    #     self.logger.info(f"Agent {self.id} has a total of {self.likes} likes.")
    #     print(f"Agent {self.id} has a total of {self.likes} likes.")

    # def add_comments(self):
    #     """Increment the comments count for the agent and print the updated total."""
    #     self.comments += 1
    #     self.logger.info(f"Agent {self.id} has a total of {self.comments} comments.")
    #     print(f"Agent {self.id} has a total of {self.comments} comments.")

    # def add_shares(self):
    #     """Increment the shares count for the agent and print the updated total."""
    #     self.shares += 1
    #     self.logger.info(f"Agent {self.id} has a total of {self.shares} shares.")
    #     print(f"Agent {self.id} has a total of {self.shares} shares.")

    # def add_folliws(self):
    #     """Increment the folliws count for the agent and print the updated total."""
    #     self.folliws += 1
    #     self.logger.info(f"Agent {self.id} has a total of {self.follows} follows.")
    #     print(f"Agent {self.id} has a total of {self.folliws} folliws.")

    


