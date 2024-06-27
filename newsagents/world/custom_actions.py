import json
from genworlds.objects.abstracts.object import AbstractObject
from genworlds.events.abstracts.event import AbstractEvent
from genworlds.events.abstracts.action import AbstractAction


class AgentWantsUpdatedStateEvent(AbstractEvent):
    event_type:str = "agent_wants_updated_state"
    description:str = "Agent wants to update its state."
    # that gives available_action_schemas, and available_entities


class WorldSendsAvailableEntitiesEvent(AbstractEvent):
    event_type:str = "world_sends_available_entities_event"
    description:str = "Send available entities."
    available_entities: dict
    news: dict


class WorldSendsAvailableEntities(AbstractAction):
    trigger_event_class = AgentWantsUpdatedStateEvent
    description:str = "Send available entities."

    def __init__(self, host_object: AbstractObject):
        super().__init__(host_object=host_object)

    def __call__(self, event: AgentWantsUpdatedStateEvent):
        self.host_object.update_entities()
        all_entities = self.host_object.entities

        objects_dict = {}
        for obj in self.host_object.objects:
            obj_dict = {
                "id": obj.id,
                "title": obj.title,  
                "content": obj.content,
                "publisher_id": obj.publisher_id,
                "category": obj.category,
                "publish_time": obj.publish_time
            }
            objects_dict[obj.id] = obj_dict

        event = WorldSendsAvailableEntitiesEvent(
            sender_id=self.host_object.id,
            available_entities=all_entities,
            target_id=event.sender_id,
            news = {
                "objects": objects_dict
            }
        )
        self.host_object.send_event(event)


class WorldSendsAvailableActionSchemasEvent(AbstractEvent):
    event_type:str = "world_sends_available_action_schemas_event"
    description:str = "The world sends the possible action schemas to all the agents."
    world_name: str
    world_description: str
    available_action_schemas: dict[str, str]


class WorldSendsAvailableActionSchemas(AbstractAction):
    trigger_event_class = AgentWantsUpdatedStateEvent
    description:str = "The world sends the possible action schemas to all the agents."

    def __init__(self, host_object: AbstractObject):
        super().__init__(host_object=host_object)

    def __call__(self, event: AgentWantsUpdatedStateEvent):
        self.host_object.update_action_schemas()
        self.host_object.update_entities()
        all_action_schemas = self.host_object.action_schemas
        all_entities = self.host_object.entities
        to_delete = []
        for action_schema in all_action_schemas:
            if all_entities[action_schema.split(":")[0]].entity_type == "AGENT" and action_schema.split(":")[0] != event.sender_id:
                to_delete.append(action_schema)

            if all_entities[action_schema.split(":")[0]].entity_type == "WORLD":
                to_delete.append(action_schema)
        
            if action_schema == f"{event.sender_id}:AgentListensEvents":
                to_delete.append(action_schema)

        for action_schema in to_delete:
            del all_action_schemas[action_schema]
            
        event = WorldSendsAvailableActionSchemasEvent(
            sender_id=self.host_object.id,
            target_id=event.sender_id,
            world_name=self.host_object.name,
            world_description=self.host_object.description,
            available_action_schemas=all_action_schemas,
        )
        self.host_object.send_event(event)

class UpdateAgentAvailableEntities(AbstractAction):
    trigger_event_class = WorldSendsAvailableEntitiesEvent
    description: str = "Update the available entities in the agent's state."

    def __init__(self, host_object: AbstractObject):
        super().__init__(host_object=host_object)

    def __call__(self, event: WorldSendsAvailableEntitiesEvent):
        self.host_object.state_manager.state.available_entities = (
            event.available_entities
        )
        if any(entity_data.get('entity_type') == 'OBJECT' for entity_data in self.host_object.state_manager.state.available_entities.values()):
            news_objects = event.news["objects"]
            news_data = []
            # 遍历 news_objects 字典中的每个新闻对象
            for news_id, news_info in news_objects.items():
                # 提取 news_id 和 content 属性
                news_id = news_info["id"]
                content = news_info["content"]
                # 将 news_id 和 content 添加到 news_data 列表中
                news_data.append({"news_id": news_id, "content": content})
                if isinstance(self.host_object.state_manager.state.news_content, list):
                    if content not in self.host_object.state_manager.state.news_content:
                        self.host_object.state_manager.state.news_content.append(content)
                else:
                    # 如果 news_content 不是列表，需要先处理
                    existing_content = self.host_object.state_manager.state.news_content.split(' ')
                    if content not in existing_content:
                        self.host_object.state_manager.state.news_content += ' ' + content
                # print("66666",self.host_object.state_manager.state.news_content )

            # self.host_object.send_event(
            #     AgentReceivesNewsEvent(
            #         sender_id=event.sender_id,
            #         target_id=event.target_id,
            #         news_id=news_id,
            #         news_content=content,
            #         comment_content=None
            #     )
            # )
            # print(f"Agent {self.host_object.id} receives news: {news_id}")

class UpdateAgentAvailableActionSchemas(AbstractAction):
    trigger_event_class = WorldSendsAvailableActionSchemasEvent
    description: str = "Update the available action schemas in the agent's state."

    def __init__(self, host_object: AbstractObject):
        super().__init__(host_object=host_object)

    def __call__(self, event: WorldSendsAvailableActionSchemasEvent):
        self.host_object.state_manager.state.available_action_schemas = (
            event.available_action_schemas
        )


class AgentWantsToSleepEvent(AbstractEvent):
    event_type:str = "agent_wants_to_sleep"
    description:str = "The agent wants to sleep. He has to wait for new events. The sender and the target ID is the agent's ID."


class AgentGoesToSleepEvent(AbstractEvent):
    event_type:str = "agent_goes_to_sleep"
    description:str = "The agent is waiting."


class AgentGoesToSleep(AbstractAction):
    trigger_event_class = AgentWantsToSleepEvent
    description:str = "The agent goes to sleep. He has to wait for new events. The sender and the target ID is the agent's ID."

    def __init__(self, host_object: AbstractObject):
        super().__init__(host_object=host_object)

    def __call__(self, event: AgentWantsToSleepEvent):
        self.host_object.state_manager.state.is_asleep = True
        self.host_object.state_manager.state.plan = []
        self.host_object.send_event(
            AgentGoesToSleepEvent(sender_id=self.host_object.id, target_id=None)
        )
        print("Agent goes to sleep...")


class WildCardEvent(AbstractEvent):
    event_type:str = "*"
    description:str = "This event is used as a master listener for all events."


class AgentListensEvents(AbstractAction):
    trigger_event_class = WildCardEvent
    description:str = "The agent listens to all the events and stores them in his memory."

    def __init__(self, host_object: AbstractObject):
        super().__init__(host_object=host_object)

    def __call__(self, event: dict):
        if (
            event["target_id"] == self.host_object.id
            or event["target_id"] == None
            or event["sender_id"] == self.host_object.id
        ):
            if (
                event["event_type"]
                not in self.host_object.state_manager.state.memory_ignored_event_types
            ):
                self.host_object.state_manager.memory.add_event(
                    json.dumps(event), summarize=False
                )  # takes time
            if (
                event["event_type"]
                in self.host_object.state_manager.state.wakeup_event_types
            ):
                self.host_object.state_manager.state.is_asleep = False
                print("Agent is waking up...")
