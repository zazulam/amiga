# miga
project to manage a spotify collaborative playlist between some friends

Idea: I wanted to share a playlist with friends that we can drop new/current songs we are listening to. However, I did not want to manually manage the tracks in there i.e. delete ones that were aging for too long. 

I chose to store the songs because:
1. To keep a record of any old songs that someone might want to go back to that they didn't save.
2. For potential 'end of year' spotify type wrapped analysis.



## Setup
* Create a collaborative playlist with some friends.
* Create a Spotify app in their Developer portal.
* Store the details in AWS Parameter Store.
* Create a Lambda function with environment variables for the Username(Should be your own), the name of the collaborative playlist, the table name to store the previous songs. 
* Create a Lambda Layer for the python packages, you use the packages.zip in the repo for the upload, and add it into the Lambda function.
* Make sure to enable permission for your Lambda IAM role to access SSM for Parameter Store and DynamoDB.
* Create an EventBridge to target that lambda(this is where you can set the time interval for how long the current set of tracks live in the playlist, I typically wipe every 30 days).

Runtime for Lambda and Layer is Python 3.8


Hope it helps!

@ Michael Zazula