<h1 align="center"> 🏏 T20-Score-Predictor 🏏 </h1>

<p align="center">
     <img src="./assets/T20-Cricket-App-Banner.png"/>
</p>

Welcome to the T20 Score Predictor! Stay ahead in the game, 📈 and elevate ✨ your cricket experience 🏏 with our simple prediction tool.

Currently this application is deployed for the purposes of inferring information about the **first innings of a T20 cricket match**.

<details open>
  <summary>
<h2>🌐 Streamlit Share App</h2>
  </summary>
  
**Click [here](https://t20-cricket-score-predictor-web.streamlit.app/) to try about the General Predictor Model.**

<h4>Note to user </h4>

- The Pro Version application which uses trains the model realtime is blocked in the web version.
- The Timeline of Predicted Score form can only be rendered in local execution of the application.
</details>

<details open>
  <summary>
<h2> ❇ Features </h2>
  </summary>

1. Making an estimate on the innings total of the team batting first at any stage of the innings and
2. Displaying the variation of the predicted innings total at each stage (_Availble only on the Local Application_)  
</details>

<details>
  <summary>
<h2>🖥 Instructions to run Application Locally </h2>
    </summary>
It is required to install [Streamlit](https://streamlit.io/) on your device to run this application locally.

Clone this application from github using

```git clone github.com/navindu-ds/T20-Cricket-Score-Predictor```

Refer the streamlit documentation for installation process depending on your operating system.
1. [Windows](https://docs.streamlit.io/library/get-started/installation#install-streamlit-on-windows)
2. [MacOS/Linux](https://docs.streamlit.io/library/get-started/installation#install-streamlit-on-macoslinux)

Use the following code in the streamlit supported environment to run the application

```python -m streamlit run App.py```
</details>

<details>
  <summary>
<h2>📊 Data and Model</h2>
  </summary>

The program uses Machine Learning Libraries such as 
1. sklearn
2. xgboost
to construct these estimates.

For the test data in order to train the program, ball by ball data from the matches in the Indian Premier League (IPL) from the years 2008 - 2021 May have been used. Even though most of the matches are played in India and majority of players are from a single country, I have considered using this dataset to apply for International Matches (and other league matches) for a few reasons. 
* The matches span over a decade hence we have a very large number of match and overs scenarios.
* Though all matches are played in India (barring some in South Africa and UAE) the variety in their own pitch conditions across the large country provide a variety of conditions found globally.
* The IPL provides a platform for both seasoned international players as well as young inexperienced players, hence we a large number of player profiles of all skill levels.
* The competitive nature of the IPL provides a near equal level of competitiveness to events such as a World Cup Tournament.

Our basic assusmption is that the run scoring will be independent of who the teams are, or grounds where they played, or the time period these matches were played in.

The original dataset was obtained from the following [link](https://www.kaggle.com/datasets/sneharsingh/ipl-dataset2008-may-2021).

</details>
<details> 
  <summary>
<h2>🔮 General Predictor Version </h2>
  </summary>

This model was designed to allow an easily deployable model to be used as an web application. For this purpose a generalized model using all available data was used to form the model.

</details>
<details> 
  <summary>
<h2>🔮✨ Pro Predictor Version </h2>
  </summary>
In this model design, the program will select the cases which are similar to the inputted data such as based on the overs remaining and the wickets remaining. These two features are considered as the main two parameters that effect the availability of resources for a team to score a certain total of runs. This is the same idealogy adopted by the Duckworth-Lewis-Stern method in handling match scenarios with weather related interruptions. 

It is only with the selected data, the predictive model is built. For each set of input data, it is required to rebuild a new ML model. Though it leads to higher computation costs - the results tend to be more steady than the general version.
</details>

Nevertheless, cricket is very unpredictable game which is one of the reasons it is such an enjoyable soprt to watch. Therefore more often than not match predictions will fluctuate as the match further progresses.
