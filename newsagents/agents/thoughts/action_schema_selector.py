import asyncio
import json
import re

import sys
import websockets
from typing import List, Optional
from genworlds.agents.abstracts.thought import AbstractThought
from newsagents.agents.custom_agent_state import CustomAgentState
from langchain_openai import ChatOpenAI

from pydantic import BaseModel, Field, ConfigDict
#from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.chains.structured_output import (
    create_structured_output_runnable
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from genworlds.utils.logging_factory import LoggingFile

class ActionSchemaSelectorThought(AbstractThought):
    def __init__(
        self,
        agent_state: CustomAgentState,
        openai_api_key: str,
        model_name: str = "llama3",
    ):
        self.agent_state = agent_state
        self.model_name = model_name
        self.llm = ChatOpenAI(
            model=self.model_name, openai_api_key=openai_api_key, temperature=0.1
        )
        self.logger = LoggingFile.get_logger(self.__class__.__name__)

    def run(self):
        class PlanNextAction(BaseModel):
            """Plans for the next action to be executed by the agent."""

            action_name: str = Field(
                ...,
                description="Selects the action name of the next action to be executed from the list of available action names.",
            )
            is_action_valid: bool = Field(
                ..., 
                description="Determines whether the next action is valid or not."
            )
            is_action_valid_reason: Optional[str] = Field(
                None,
                description="Then explains the rationale of whether it is valid or not valid action.",
            )
            new_plan: List[str] = Field(
                ..., 
                description="The new plan to execute to achieve the goals."
            )
            new_plan_reason: Optional[str] = Field(
                None,
                description="Then explain the rationale for why these plans were chosen.",
            )
            # class Config:
            #     arbitrary_types_allowed = True

        action_schemas_full_string = "## Available Actions: \n\n"
        for (
            action_schema_key,
            action_schema_value,
        ) in self.agent_state.available_action_schemas.items():
            action_schemas_full_string += (
                "Name: "
                # + action_schema_value.split("|")[0]
                # + "\nDescription: "
                + action_schema_key
                + "\n"
            )

        # 检查代理当前的情感和态度
        population_category = self.agent_state.population_category
        # 根据不同人群类别设置情感和态度波动范围
        category_description = population_category.get_description()

        def extract_structured_output(content):
            # Extracting the action name
                # Extracting the action name
            action_name_match = re.search(r'[aA]ction(?: [nN]ame)?: (?:\w+:)?(.+)', content)
            action_name = action_name_match.group(1).strip() if action_name_match else None
    
            # Concatenating agent name with action name
            agent_action_name = f"{self.agent_state.id}:{action_name}" if action_name else None
            
            # Extracting the validity
            validity_match = re.search(r'Validity: (.+)', content)
            validity_line = validity_match.group(1).strip() if validity_match else None
            is_action_valid = validity_line.lower() == 'true' if validity_line else False
            
            # Extracting the validity reason
            validity_reason_match = re.search(r'Reason(?: \(If validity is true\))?: (.+)', content)
            is_action_valid_reason = validity_reason_match.group(1).strip() if validity_reason_match else None

            # Extracting the number
            number_match = re.search(r'Number: ([\d,]+)', content)
            number = int(number_match.group(1).replace(',', '').strip()) if number_match else None

            # Extracting the new plan
            new_plan_start = content.find("Updated plan:") + len("Updated plan:\n")
            new_plan_end = content.find("Note:", new_plan_start)
            if new_plan_end == -1:
                new_plan_end = len(content)
            new_plan_text = content[new_plan_start:new_plan_end].strip()
            
            # Extracting only the valid plan steps starting with a number
            plan_lines = new_plan_text.split('\n')
            new_plan = []
            for line in plan_lines:
                stripped_line = line.strip()
                if re.match(r'^\d+\.', stripped_line):  # Match lines starting with a number followed by a dot
                    new_plan.append(stripped_line)
            
            # No explicit new plan reason in the content, keeping it as None
            new_plan_reason = None
            self.agent_state.num_temp = number
            new_plan_properties = {
                "action_name": agent_action_name,
                "is_action_valid": is_action_valid,
                "is_action_valid_reason": is_action_valid_reason,
                "number": number,
                "new_plan": new_plan,
                "new_plan_reason": new_plan_reason
            }

            return new_plan_properties
        
        def update_parameter_based_on_action(new_plan_properties):
            action_name = new_plan_properties["action_name"]
            number = new_plan_properties["number"]

            if not action_name:
                print("No action specified.")
                return

            # Define the mapping of action names to their corresponding update functions
            action_mapping = {
                "AgentViewsNewsAndUpdateStateAction": self.agent_state.update_news_views,
                "AgentLikesNewsAction": self.agent_state.update_news_likes,
                "AgentCommentsOnNewsAction": self.agent_state.update_news_comments,
                "AgentSharesNewsAction": self.agent_state.update_news_shares,
                "AgentFollowsNewsAction": self.agent_state.update_news_follows
            }

            # Extract the base action name (in case the action name includes the agent's ID)
            base_action_name = action_name.split(":")[-1].strip()

            # Get the corresponding update function from the action mapping
            update_function = action_mapping.get(base_action_name)

            if update_function:
                update_function(number)
            else:
                print(f"Unknown action: {base_action_name}")

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are {agent_name}, {agent_description}.\n"),
                (
                    "system",
                    "You are embedded in a simulated world with those properties {agent_world_state}\n",
                ),
                # ("system", "Those are your goals: \n{goals}\n"),
                # (
                #     "system",
                #     "And this is the previous plan to achieve the goals: \n{plan}\n",
                # ),
                # (
                #     "system",
                #     "Here is your memories of all the events that you remember from being in this simulation: \n{memory}\n",
                # ),
                (
                    "system",
                    "Those are the available actions that you can choose from: \n{available_actions}\n",
                ),
                (
                    "system",
                    "Your current emotion is: {emotions}. \nYour current attitude is: {attitudes}."
                ),
                (
                    "system", "The news content you have received is: {news_content}. "
                ),
                (
                    "system", "Your group currently has {news_views} views, {news_likes} likes, {news_comments} comments,{news_follows} follows, and {news_shares} shares for this news."
                ),
                (
                    "system",
                    "Considering your population category ({population_category}), individuals exhibit the following characteristics: {category_description}."
                ),
                ("human", "{footer}\n"),
            ]
        ).partial(schema=PlanNextAction.model_json_schema())

        input_context = {
            "agent_name": self.agent_state.name,
            "agent_description": self.agent_state.description,
            "agent_world_state": self.agent_state.host_world_prompt,
            #"goals": self.agent_state.goals,
            # "plan": self.agent_state.plan,
            #"memory": self.agent_state.last_retrieved_memory,
            "available_actions": action_schemas_full_string,
            "emotions": self.agent_state.emotion,
            "attitudes": self.agent_state.attitude,
            "news_content": self.agent_state.news_content,
            "news_views": self.agent_state.news_views,
            "news_likes": self.agent_state.news_likes,
            "news_comments": self.agent_state.news_comments,
            "news_follows": self.agent_state.news_follows,
            "news_shares": self.agent_state.news_shares,
            "category_description": category_description,
            "population_category": self.agent_state.population_category,
            "footer": """
                1. Based on factors such as sentiment, attitude index, news content, your views, likes, comments, follows, shares, your attribute characteristics, and the number of groups, choose the next action. This action must be one of the available actions based on the previous context. Also, determine if this action is effective, and if not, explain why;
                2. Ensure that the received (views, likes, shares, comments, follows) values ​​must satisfy the following formula to match the real world: views ≫ likes ≫ shares ≥ comments ≥ follows, and the value of views must always be the greatest. If any condition is not met, the corresponding available action is performed and the value is adjusted accordingly to match the formula;
                3. Based on the total number of your crowd, infer how many people choose this action at this point in time. This value is much smaller than the total number of your crowd;
                4. Answers should follow the following format:
                    Action: {Action name}
                    Validity: {True/False}
                    Reason (If validity is true): {reason}
                    Number: {Integer}
                    Updated plan: {List available actions with serial numbers}
                """
        } #3. State a new updated plan that you want to execute to achieve your goals.
        #2. If both the emotion and attitude values are 0, the next action must be AgentViewsNewsAndUpdateStateAction, otherwise it should be other available actions;
        #print("action_schemas_full_string: ",action_schemas_full_string)
        # 2. Before taking any other action (like, comment, share, or follow), you must view the news first (view count cannot be 0). Ensure that over multiple responses, all the following actions are performed in sequence: AgentViewsNewsAndUpdateStateAction, AgentLikesNewsAction, AgentCommentsOnNewsAction, AgentSharesNewsAction, and AgentFollowsNewsAction.

        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser
        res = chain.invoke(input_context)
        print("res: ",res)
        response = extract_structured_output(res)
        update_parameter_based_on_action(response)
        self.logger.info(f"Action: {response}")
        response = PlanNextAction.model_validate(response)

        print(f"{self.agent_state.id} currently has {self.agent_state.news_views} views, {self.agent_state.news_likes} likes, {self.agent_state.news_comments} comments, {self.agent_state.news_follows} follows, and {self.agent_state.news_shares} shares for this news.")
        self.logger.info(f"{self.agent_state.id} currently has {self.agent_state.news_views} views, {self.agent_state.news_likes} likes, {self.agent_state.news_comments} comments, {self.agent_state.news_follows} follows, and {self.agent_state.news_shares} shares for this news.")
        
        return response.action_name, response.new_plan

        # Chain construction and extraction of structured output when using opanai key

        # chain = create_structured_output_runnable(
        #     PlanNextAction.schema(), self.llm, prompt  #, verbose=True
        # )
        # structured_llm = create_structured_output_runnable(
        #     PlanNextAction.schema(),
        #     self.llm,
        #     mode="openai-json",
        #     enforce_function_usage=False
        # )
        # chain = prompt | structured_llm
        # #chain = structured_llm