from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.management import Cloudwatch
from diagrams.generic.device import Mobile
from diagrams.aws.database import Dynamodb

with Diagram("Top Song Recommendations", show=False):

    event_trigger = Cloudwatch("Event Trigger")
    recommender = Lambda("Song Recommendations")
    my_mobile = Mobile("My Phone")
    song_db = Dynamodb("Song database")

    event_trigger >> recommender << song_db
    recommender >> my_mobile