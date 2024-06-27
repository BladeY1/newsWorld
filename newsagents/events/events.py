# action.py

import json
from time import sleep
from genworlds.objects.abstracts.object import AbstractObject
from genworlds.events.abstracts.action import AbstractAction
from genworlds.events.abstracts.event import AbstractEvent, NewsEvent
from genworlds.utils.logging_factory import LoggingFile

# 定义事件
class AgentReceivesNewsEvent(NewsEvent):
    event_type: str = "agent_receives_news_event"
    description: str = "An agent receives a piece of news."

class AgentViewsNewsAndUpdateStateEvent(NewsEvent):
    event_type: str = "agent_views_news_and_updates_state_event"
    description: str = "Agent views a piece of news and updates its state."
    temp_number: int

class AgentHasUpdatedStateBasedOnNewsEvent(NewsEvent):
    event_type: str = "agent_has_updated_state_based_on_news_event"
    description: str = "Agent has updated its state based on news."

class AgentLikesNewsEvent(NewsEvent):
    event_type: str = "agent_likes_news_event"
    description: str = "An agent likes a piece of news."
    temp_number: int

class AgentCommentsOnNewsEvent(NewsEvent):
    event_type: str = "agent_comments_on_news_event"
    description: str = "An agent comments on a piece of news."
    temp_number: int

class AgentSharesNewsEvent(NewsEvent):
    event_type: str = "agent_shares_news_event"
    description: str = "An agent shares a piece of news."
    temp_number: int

class AgentFollowsNewsEvent(NewsEvent):
    event_type: str = "agent_follows_news_event"
    description: str = "An agent follows a piece of news."
    temp_number: int


# 定义动作
class AgentViewsNewsAndUpdateStateAction(AbstractAction):
    trigger_event_class = AgentReceivesNewsEvent
    description: str = "Agent views a piece of news and updates its state."

    def __init__(self, host_object):
        super().__init__(host_object)
        self.logger = LoggingFile.get_logger(self.__class__.__name__)

    def __call__(self, event: AgentReceivesNewsEvent):
        updated_emotion_and_attitude = self.host_object.action_planner.update_agent_state_based_on_news(self.host_object.state_manager, event)
        # 触发AgentViewsNewsAndUpdateStateEvent事件
        event = AgentViewsNewsAndUpdateStateEvent(
                sender_id=self.host_object.id,
                target_id=event.target_id,
                news_id=event.news_id,
                news_content=event.news_content,
                temp_number = self.host_object.state_manager.state.num_temp,
                comment_content=event.comment_content
            )
        self.host_object.send_event(event)
        self.host_object.state_manager.memory.add_event(event.model_dump_json(), summarize=True)

        self.logger.info(f"Agent {self.host_object.id} has a total of {self.host_object.state_manager.state.news_views} views.")

        self.logger.info(f"Agent {self.host_object.id} updates state based on news {event.news_id}: {updated_emotion_and_attitude.emotion, updated_emotion_and_attitude.attitude}")
        print(f"Agent {self.host_object.id} updates state based on news {event.news_id}: {updated_emotion_and_attitude.emotion, updated_emotion_and_attitude.attitude}")


class AgentLikesNewsAction(AbstractAction):
    trigger_event_class = AgentHasUpdatedStateBasedOnNewsEvent
    description: str = "Agent likes a piece of news."

    def __init__(self, host_object):
        super().__init__(host_object)
        self.logger = LoggingFile.get_logger(self.__class__.__name__)

    def __call__(self, event: AgentHasUpdatedStateBasedOnNewsEvent):
        event = AgentLikesNewsEvent(
                sender_id=self.host_object.id,
                target_id=None,
                news_id=event.news_id,
                news_content=event.news_content,
                temp_number = self.host_object.state_manager.state.num_temp,
                comment_content=event.comment_content
            )
        self.host_object.send_event(event)
        self.host_object.state_manager.memory.add_event(event.model_dump_json(), summarize=True)
        
        self.logger.info(f"Agent {self.host_object.id} has a total of {self.host_object.state_manager.state.news_likes} likes.")

        self.logger.info(f"{self.host_object.name} is optimistic and decides to like the news.")
        print(f"{self.host_object.name} is optimistic and decides to like the news.")


class AgentCommentsOnNewsAction(AbstractAction):
    trigger_event_class = AgentHasUpdatedStateBasedOnNewsEvent
    description: str = "Agent comments on a piece of news."

    def __init__(self, host_object):
        super().__init__(host_object)
        self.logger = LoggingFile.get_logger(self.__class__.__name__)

    def __call__(self, event: AgentHasUpdatedStateBasedOnNewsEvent):
        # 根据情感和态度执行评论操作
        if (
            self.host_object.state_manager.state.emotion["anger"] > 0.5
            or self.host_object.state_manager.state.emotion["sadness"] > 0.7
            or self.host_object.state_manager.state.emotion["happiness"] > 0.6
        ):
            # 获取代理的情感
            emotions = self.host_object.state_manager.state.emotion
            # 根据不同的情感选取最高的情感指数发表相应的评论
            max_emotion = max(emotions, key=lambda e: emotions[e])
            if max_emotion == "anger":
                comment = "This news makes me angry!"
            elif max_emotion == "sadness":
                comment = "So sad to hear this..."
            elif max_emotion == "happiness":
                comment = "What a joyful news!"
            else:
                comment = "Interesting."

            event = AgentCommentsOnNewsEvent(
                    sender_id=self.host_object.id,
                    target_id=event.target_id,
                    news_id=event.news_id,
                    news_content=event.news_content,
                    temp_number = self.host_object.state_manager.state.num_temp,
                    comment_content=comment
                )  
            self.host_object.send_event(event)
            self.host_object.state_manager.memory.add_event(event.model_dump_json(), summarize=True)

            self.logger.info(f"Agent {self.host_object.id} has a total of {self.host_object.state_manager.state.news_comments} comments.")
            
            self.logger.info(f"Agent {self.host_object.id} comments on news {event.news_id}: {comment}.")
            print(f"Agent {self.host_object.id} comments on news {event.news_id}: {comment}.")


class AgentSharesNewsAction(AbstractAction):
    trigger_event_class = AgentHasUpdatedStateBasedOnNewsEvent
    description: str = "Agent shares a piece of news."

    def __init__(self, host_object):
        super().__init__(host_object)
        self.logger = LoggingFile.get_logger(self.__class__.__name__)

    def __call__(self, event: AgentHasUpdatedStateBasedOnNewsEvent):
        event =  AgentSharesNewsEvent(
                sender_id=self.host_object.id,
                target_id=event.target_id,
                news_id=event.news_id,
                news_content=event.news_content,
                temp_number = self.host_object.state_manager.state.num_temp,
                comment_content=event.comment_content
            )
        self.host_object.send_event(event)
        self.host_object.state_manager.memory.add_event(event.model_dump_json(), summarize=True)

        self.logger.info(f"Agent {self.host_object.id} has a total of {self.host_object.state_manager.state.news_shares} shares.")

        self.logger.info(f"Agent {self.host_object.id} shares news {event.news_id}: {event.news_content}")
        print(f"Agent {self.host_object.id} shares news {event.news_id}: {event.news_content}")


class AgentFollowsNewsAction(AbstractAction):
    trigger_event_class = AgentHasUpdatedStateBasedOnNewsEvent
    description: str = "Agent follows a piece of news."

    def __init__(self, host_object):
        super().__init__(host_object)
        self.logger = LoggingFile.get_logger(self.__class__.__name__)

    def __call__(self, event: AgentHasUpdatedStateBasedOnNewsEvent):
        event =  AgentFollowsNewsEvent(
                sender_id=self.host_object.id,
                target_id=event.target_id,
                news_id=event.news_id,
                news_content=event.news_content,
                temp_number = self.host_object.state_manager.state.num_temp,
                comment_content=event.comment_content
            )
        self.host_object.send_event(event)
        self.host_object.state_manager.memory.add_event(event.model_dump_json(), summarize=True)

        self.logger.info(f"Agent {self.host_object.id} has a total of {self.host_object.state_manager.state.news_follows} follows.")

        self.logger.info(f"Agent {self.host_object.id} follows news {event.news_id}: {event.news_content}")
        print(f"Agent {self.host_object.id} follows news {event.news_id}: {event.news_content}")
