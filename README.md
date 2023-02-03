# T20-Score-Predictor
A machine learning program to estimate the completed innings score in a T20 cricket match.

This program is designed to aid cricket fans make a fair estimate of how the cricket match will progress by;
   1. making an estimate on the innings total of the team batting first and,
   2. providing an indicator of how well the team batting second is chasing the target,
at a midway stage of the innings.

The program is coded with Python 3 and uses Machine Learning Libraries such as
  1. sklearn
  2. xgboost to construct these estimates.
 
For the test data in order to train the program, ball by ball data from the matches in the Indian Premier League (IPL) from the years 2008 - 2021 May have been used. Even though most of the matches are played in India and majority of players are from a single country, I have considered using this dataset to apply for International Matches (and other league matches) for a few reasons.

   1. The matches span over a decade hence we have a very large number of match and overs scenarios.
   2. Though all matches are played in India (barring some in South Africa and UAE) the variety in their own pitch conditions allow all type of scenarios.
   3. The IPL provides a platform for both seasoned international players as well as young inexperienced players, hence we a large number of player profiles of all types of skills.
   4. The competitive nature of the IPL provides a near equal competitiveness to events such as a World Cup Tournament.
   5. Non Availability of Datasets for all International Matches.

This dataset was found on Kaggle. (https://www.kaggle.com/datasets/sneharsingh/ipl-dataset2008-may-2021/code)

Our basic assusmption is that the run scoring will be independent of who the teams are, or grounds where they played, or when they have played these matches used in the test data.

Nevertheless, cricket is very unpredictable game which is one of the reasons it is such an enjoyable soprt to watch. Therefore more often than not match predictions will fluctuate as the match further progresses.
