from enum import Enum

class NewsCategory(str, Enum):
    Education = "Education News"
    BUSINESS = "Business News"
    TECHNOLOGY = "Technology News"
    CULTURE = "Culture News"
    SPORTS = "Sports News"
    HEALTH = "Health News"
    ENTERTAINMENT = "Entertainment News"
    ENVIRONMENT = "Environmental News"
    POLITICAL = "Political News"
    ECONOMIC = "Economic News"
    SOCIAL = "Social News"

class World:
    def __init__(self, name, description, id):
        self.name = name
        self.description = description
        self.id = id

# Define the mapping between NewsCategory and their corresponding worlds
world_map = {
    NewsCategory.Education: World(
        name="EducationNewsWorld",
        description="""A social network focused on news dissemination within the education community. It is a platform where users from the education circle can share, comment, follow, and engage with news articles and other media content. The network is designed to facilitate conversations around current events, research, and other topics of interest within the education community.""",
        id="EducationNews-world"
    ),
    NewsCategory.BUSINESS: World(
        name="BusinessNewsWorld",
        description="""A social network focused on news dissemination within the business community. It is a platform where users from the business circle can share, comment, follow, and engage with news articles and other media content. The network is designed to facilitate conversations around current events, research, and other topics of interest within the business community.""",
        id="BusinessNews-world"
    ),
    NewsCategory.TECHNOLOGY: World(
        name="TechnologyNewsWorld",
        description="""A social network focused on news dissemination within the technology community. It is a platform where users from the technology circle can share, comment, follow, and engage with news articles and other media content. The network is designed to facilitate conversations around current events, research, and other topics of interest within the technology community.""",
        id="TechnologyNews-world"
    ),
    NewsCategory.CULTURE: World(
        name="CultureNewsWorld",
        description="""A social network focused on news dissemination within the cultural community. It is a platform where users from the cultural circle can share, comment, follow, and engage with news articles and other media content. The network is designed to facilitate conversations around current events, research, and other topics of interest within the cultural community.""",
        id="CultureNews-world"
    ),
    NewsCategory.SPORTS: World(
        name="SportsNewsWorld",
        description="""A social network focused on news dissemination within the sports community. It is a platform where users from the sports circle can share, comment, follow, and engage with news articles and other media content. The network is designed to facilitate conversations around current events, research, and other topics of interest within the sports community.""",
        id="SportsNews-world"
    ),
    NewsCategory.HEALTH: World(
        name="HealthNewsWorld",
        description="""A social network focused on news dissemination within the health community. It is a platform where users from the health circle can share, comment, follow, and engage with news articles and other media content. The network is designed to facilitate conversations around current events, research, and other topics of interest within the health community.""",
        id="HealthNews-world"
    ),
    NewsCategory.ENTERTAINMENT: World(
        name="EntertainmentNewsWorld",
        description="""A social network focused on news dissemination within the entertainment community. It is a platform where users from the entertainment circle can share, comment, follow, and engage with news articles and other media content. The network is designed to facilitate conversations around current events, research, and other topics of interest within the entertainment community.""",
        id="EntertainmentNews-world"
    ),
    NewsCategory.ENVIRONMENT: World(
        name="EnvironmentalNewsWorld",
        description="""A social network focused on news dissemination within the environmental community. It is a platform where users from the environmental circle can share, comment, follow, and engage with news articles and other media content. The network is designed to facilitate conversations around current events, research, and other topics of interest within the environmental community.""",
        id="EnvironmentalNews-world"
    ),
    NewsCategory.POLITICAL: World(
        name="PoliticalNewsWorld",
        description="""A social network focused on news dissemination within the political community. It is a platform where users from the political circle can share, comment, follow, and engage with news articles and other media content. The network is designed to facilitate conversations around current events, research, and other topics of interest within the political community.""",
        id="PoliticalNews-world"
    ),
    NewsCategory.ECONOMIC: World(
        name="EconomicNewsWorld",
        description="""A social network focused on news dissemination within the economic community. It is a platform where users from the economic circle can share, comment, follow, and engage with news articles and other media content. The network is designed to facilitate conversations around current events, research, and other topics of interest within the economic community.""",
        id="EconomicNews-world"
    ),
    NewsCategory.SOCIAL: World(
        name="SocialNewsWorld",
        description="""A social network focused on news dissemination within the social community. It is a platform where users from the social circle can share, comment, follow, and engage with news articles and other media content. The network is designed to facilitate conversations around current events, research, and other topics of interest within the social community.""",
        id="SocialNews-world"
    ),
}

def get_world_for_category(category: NewsCategory) -> World:
    return world_map.get(category, None)

# Example usage
if __name__ == "__main__":
    category = NewsCategory.ACADEMIC
    world = get_world_for_category(category)
    if world:
        print(f"World Name: {world.name}")
        print(f"Description: {world.description}")
        print(f"ID: {world.id}")
    else:
        print("No world found for the given category.")
