# Station-Discourse-to-Canny-Migration
Migration of the Station community on Discourse to Canny.io

This code migrated data from the Station Discourse Community (community.getstation.com) to the new Canny community (feedback.getstation.com).

In total: 
- 5,973 users migrated
- 1,005 topics migrated
- 9,000+ comments migrated

Main scripts:

- users.py: Migrate all users from Discourse to Canny
- list_boards_canny.py: Fetches the board IDs from Canny in order to push data on the right boards
- general_topics.py: Migrates all topics in the "General" board to Canny "Bugs & Support"
- general_comments.py: Migrates all comments in the "General" board to Canny "Bugs & Support"
- features_topics.py: Migrates all topics in the "Feature Requests" board to Canny "Features Requests"
- features_comments.py: Migrates all comments in the "Feature Requests" board to Canny "Feature Requests"
- developer_topics.py: Migrates all topics in the "Developers" board to Canny "Developers"
- developer_comments.py: Migrates all comments in the "Developers" board to Canny "Developers"
- design_topics.py: Migrates all topics in the "UX & Design" board to Canny "Feature Requests"
- design_comments.py: Migrates all comments in the "UX & Design" board to Canny "Feature Requests"
- bugs_topics.py: Migrate all topics in the "Bugs, Support & Troubleshooting" board to Canny "Bugs & Support"
- bugs_comments.py: Migrate all comments in the "Bugs, Support & Troubleshooting" board to Canny "Bugs & Support"

Dictionaries used in the different scripts to match data between the two APIs:
- canny_topics_general.json
- canny_topics_features.json
- canny_topics_developer.json
- canny_topics_design.json
- canny_topics_bugs.json
- canny_topics_bugs2.json


It was not possible to migrate the timestamps of the posts through the POST endpoints on Canny. Hence, we provided a CSV with the topics timestamps to the Canny team that wrote their own script in order to update the dates.
Scripts for timestamps:
- csv_topics_timestamps.py: timestamps for the topics
- csv_comments_timestamps.py: timestamps for the comments

The CSV exports for the timestamps:
- comments_list_bugs.csv: 
- comments_list_bugs2.csv: 
- comments_list_developers.csv:
- comments_list_features.csv: 
- comments_list_features2.csv: 
- comments_list_features.csv: 

Finally, we pulled the list of all users migrated to Canny in CSV in order to send them an email campaign:
- csv_users.py 


