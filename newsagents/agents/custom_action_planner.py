from datetime import datetime
import json
import sys
import threading
from time import sleep
from typing import List, Dict, Any, Tuple
from genworlds.agents.abstracts.action_planner import AbstractActionPlanner
from genworlds.agents.abstracts.thought import AbstractThought
from genworlds.events.abstracts.event import AbstractEvent, NewsEvent
from newsagents.events.events import AgentReceivesNewsEvent
from newsagents.agents.custom_agent_state import CustomAgentState 
from newsagents.agents.custom_agent_state import (
    CustomAgentState,
    PopulationCategory
)
from newsagents.agents.custom_state_manager import CustomStateManager

from genworlds.agents.abstracts.agent import AbstractAgent
from newsagents.agents.thoughts.action_schema_selector import ActionSchemaSelectorThought
from newsagents.agents.thoughts.event_filler import EventFillerThought
from newsagents.agents.thoughts.emotion_attitude_builder import EmotionAttitudeBuilderThought
from genworlds.agents.abstracts.thought_action import ThoughtAction
from genworlds.utils.schema_to_model import json_schema_to_pydantic_model

class CustomActionPlanner(AbstractActionPlanner):
    """This action planner selects the action schema with the highest priority and fills the event parameters with the highest priority."""

    def __init__(
        self,
        host_agent: AbstractAgent ,
        openai_api_key,
        initial_agent_state: CustomAgentState,
        other_thoughts: List[AbstractThought] = [],
        model_name: str = "llama3",
    ):
        self.host_agent = host_agent
        self.lock = threading.Lock()
        action_schema_selector = ActionSchemaSelectorThought(
            openai_api_key=openai_api_key,
            agent_state=initial_agent_state,
            model_name=model_name,
        )
        event_filler = EventFillerThought(
            openai_api_key=openai_api_key,
            agent_state=initial_agent_state,
            model_name=model_name,
        )
        emotion_attitude_builder = EmotionAttitudeBuilderThought(
            openai_api_key=openai_api_key,
            agent_state=initial_agent_state,
            model_name=model_name,
        )
        other_thoughts = other_thoughts
        super().__init__(
            action_schema_selector,
            event_filler,
            emotion_attitude_builder,
            other_thoughts,
        )

    def __repr__(self):
        print(self.host_agent.name)
        return f"CustomActionPlanner(action_schema_selector={self.action_schema_selector}, event_filler={self.event_filler}, other_thoughts={self.other_thoughts}, host_agent={self.host_agent})"

    def plan_next_action(self, state: CustomAgentState) -> Tuple[str, NewsEvent]:
        if len(state.current_action_chain) > 0:
            action_schema = state.current_action_chain.pop(0)
            trigger_event = self.fill_triggering_event(action_schema, state)
            return action_schema, trigger_event
        action_schema = self.select_next_action_schema(state)
        trigger_event = self.fill_triggering_event(action_schema, state)
        return action_schema, trigger_event

    def select_next_action_schema(self, state: CustomAgentState) -> str:
        # call action_schema_selector thought with the correct parameters
        self.lock.acquire()
        try:
            (
                next_action_schema,
                updated_plan,
            ) = self.action_schema_selector.run()  # gives enum values
        finally:
            self.lock.release()    
        state.plan = updated_plan
        if next_action_schema in [el[0] for el in state.action_schema_chains]:
            state.current_action_chain = state.action_schema_chains[
                [el[0] for el in state.action_schema_chains].index(next_action_schema)
            ][1:]
        return next_action_schema

    def fill_triggering_event(
        self, next_action_schema: str, state: CustomAgentState
    ) -> Dict[str, Any]:
        # check if is a thought action and compute the missing parameters
        if next_action_schema.startswith(self.host_agent.id):
            next_action = [
                action
                for action in self.host_agent.actions
                if next_action_schema == action.action_schema[0]
            ][0]
            trigger_event_class = next_action.trigger_event_class
            if isinstance(next_action, ThoughtAction):
                for param in next_action.required_thoughts:
                    thought_class = next_action.required_thoughts[param]
                    thought = thought_class(self.host_agent.state_manager.state)
                    state.other_thoughts_filled_parameters[param] = thought.run()

        else:
            trigger_event_class_schema = json.loads(
                self.host_agent.state_manager.state.available_action_schemas[
                    next_action_schema
                ].split("|")[-1]
            )
            trigger_event_class = json_schema_to_pydantic_model(
                trigger_event_class_schema
            )
        self.lock.acquire()
        try:
            trigger_event: NewsEvent = self.event_filler.run(trigger_event_class)
        finally:
            self.lock.release()    
        trigger_event.created_at = datetime.now().isoformat()
        return trigger_event
    

    # 代理根据接收到的新闻更新状态函数
    def update_agent_state_based_on_news(self, state_manager: CustomStateManager, event: AgentReceivesNewsEvent) -> CustomAgentState:
        news_content = event.news_content
         # call emotion_attitude_builder thought with the correct parameters
        self.lock.acquire()
        try:   
            (
                emotions, 
                attitudes
            ) = self.host_agent.action_planner.emotion_attitude_builder.run(news_content)  # gives
        finally:
            self.lock.release()
        # 检查 emotions 和 attitudes 是否不为空
        if emotions and attitudes:
            state_manager.state.emotion = emotions
            state_manager.state.attitude = attitudes

        return state_manager.state