import json
from typing import List

from genworlds.objects.abstracts.object import AbstractObject
from genworlds.simulation.sockets.handlers.event_handler import SimulationSocketEventHandler
from newsagents.events.events import AgentCommentsOnNewsEvent, AgentFollowsNewsEvent, AgentLikesNewsEvent, AgentSharesNewsEvent, AgentViewsNewsAndUpdateStateEvent  
from genworlds.utils.logging_factory import LoggingFile

# 每个新闻对象都会具有类别、发布时间、浏览量、来源、标签、点赞数、评论数和分享数的属性。
class NewsObject(AbstractObject):
    event_class_dict = {
        "agent_views_news_and_updates_state_event": AgentViewsNewsAndUpdateStateEvent,
        "agent_likes_news_event": AgentLikesNewsEvent,
        "agent_comments_on_news_event": AgentCommentsOnNewsEvent,
        "agent_shares_news_event": AgentSharesNewsEvent,
        "agent_follows_news_event": AgentFollowsNewsEvent,
    }
    def __init__(
        self,
        id: str,
        title: str,
        content: str,
        publisher_id: str,
        category: str,
        publish_time: str,
        views: int = 0,
        source: str = None,
        tags: List[str] = [],
        likes: int = 0,
        comments: int = 0,
        shares: int = 0,
        follows: int = 0,
    ):
        """
        Represents a news object in the simulation.
        Args:
            id (str): The unique identifier of the news.
            title (str): The title of the news.
            content (str): The content/body of the news.
            publisher_id (str): The identifier of the agent who published the news.
            category (str): The category of the news.
            publish_time (str): The time when the news was published.
            views (int, optional): The number of views/views of the news. Defaults to 0.
            source (str, optional): The source of the news. Defaults to None.
            tags (List[str], optional): The tags associated with the news. Defaults to [].
            likes (int, optional): The number of likes/likes of the news. Defaults to 0.
            comments (int, optional): The number of comments/comments on the news. Defaults to 0.
            shares (int, optional): The number of shares/shares of the news. Defaults to 0.
        """
        super().__init__(
            name="News",
            id=id,
            description=f"News: {title}",
            actions=[]
        )

        self.category = category
        self.publish_time = publish_time
        self.views = views
        self.source = source
        self.tags = tags
        self.follows = follows
        self.likes = likes
        self.comments = comments
        self.shares = shares

        self.title = title
        self.content = content
        self.publisher_id = publisher_id
        self.event_listeners = []

        self.logger = LoggingFile.get_logger(self.__class__.__name__)

         # Register event listeners
        self.register_event_listener(AgentViewsNewsAndUpdateStateEvent, self.handle_view_event)
        self.register_event_listener(AgentLikesNewsEvent, self.handle_like_event)
        self.register_event_listener(AgentCommentsOnNewsEvent, self.handle_comment_event)
        self.register_event_listener(AgentSharesNewsEvent, self.handle_share_event)
        self.register_event_listener(AgentFollowsNewsEvent, self.handle_follow_event)

    def register_event_listener(self, event_type, listener):
        """
        Register an event listener for a specific event type.
        """
        self.event_listeners.append((event_type, listener))

    def unregister_event_listener(self, event_type, listener):
        """
        Unregister an event listener for a specific event type.
        """
        if (event_type, listener) in self.event_listeners:
            self.event_listeners.remove((event_type, listener))
        else:
            print(f"Listener for event type {event_type} not found.")

    def receive_event(self, event):
        """
        Simulates receiving an event.
        """
        event_type = event["event_type"]
        event_class = self.event_class_dict.get(event_type)
        for listener_event_class, listener in self.event_listeners:
            if listener_event_class == event_class:
                listener(event)

    def handle_view_event(self, event):
        if event["news_id"] == self.id:
            self.views += event['temp_number']
            self.logger.info(f"News {self.id} received a view. Total views: {self.views}")
            print(f"News {self.id} received a view. Total views: {self.views}")

    def handle_like_event(self, event):
        if event["news_id"] == self.id:
            self.likes += event['temp_number']
            self.logger.info(f"News {self.id} received a like. Total likes: {self.likes}")
            print(f"News {self.id} received a like. Total likes: {self.likes}")
            

    def handle_comment_event(self, event):
        if event["news_id"] == self.id:
            self.comments += event['temp_number']
            self.logger.info(f"News {self.id} received a comment. Total comments: {self.comments}")
            print(f"News {self.id} received a comment. Total comments: {self.comments}")

    def handle_share_event(self, event):
        if event["news_id"] == self.id:
            self.shares += event['temp_number']
            self.logger.info(f"News {self.id} was shared. Total shares: {self.shares}")
            print(f"News {self.id} was shared. Total shares: {self.shares}")

    def handle_follow_event(self, event):
        if event["news_id"] == self.id:
            self.follows += event['temp_number']
            self.logger.info(f"News {self.id} was followed. Total follows: {self.follows}")
            print(f"News {self.id} was followed. Total follows: {self.follows}")

    def process_event(self, event):
        """
        Override process_event to include handling in NewsObject.
        """
        super().process_event(event)  # Call the parent class's process_event
        self.receive_event(event)  # Handle the event in NewsObject


    def add_news(self, news_item: str):
        self.news.append(news_item)

    def remove_news(self, news_item: str):
        self.news.remove(news_item)
