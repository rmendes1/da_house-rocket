<h1 align="center">
    <img alt="HouseRocketProj" title="#HouseRocket" src="img/house_rocket.png" />
</h1>

<h4 align="center"> 
	🚧 HouseRocketProj 1.0 🚀 still building... 🚧
</h4>

<p align="center">
  <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/rmendes1/house-rocket?color=%2304D361">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/rmendes1/house-rocket">
	
  
  <a href="https://github.com/rmendes1/house-rocket/commits/main">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/rmendes1/house-rocket">
  </a>

  <img alt="License" src="https://img.shields.io/badge/license-MIT-brightgreen">
</p>

# Table of Contents
<p align="center">
  <a href="#description">Description</a> •
  <a href="#dataset">Dataset</a> •
  <a href="#tools">Tools</a> •
  <a href="#steps">Steps</a> •  
  <a href="#business-hypotheses">Business Hypotheses</a> •
  <a href="#conclusion">Conclusion</a>
  <a href="#next-steps">Next Steps</a>
  <a href="#license">License</a>
</p>


# **Description**



<a href="https://share.streamlit.io/rmendes1/house-rocket/main/dashboard.py">
  <img alt="Made by rmendes1" src="https://img.shields.io/badge/Acess%20Dashboard%20-Streamlit-%2304D361">
</a>



House Rocket is a fictional company that works with Real Estates purchase and sale. The best business opportunities must be found and the strategy is to buy estates in great condition at low prices and sell those properties with higher price. The estates attributes make them more or less appealing depending on their characteristics. Thus, the attractiveness of the properties may be influenced by their attributes, and therefore, their price can vary. 


With that in mind, some questions must be answered:

1. What are the properties that the company should buy and for what price?
2. What is the best time to sell the property and the best sales price?

# **Dataset**
- The dataset for this project can be found at Kaggle: https://www.kaggle.com/harlfoxem/housesalesprediction/discussion/207885 
- This dataset contains house sale prices for King County, which includes Seattle. It includes houses sold between May 2014 and May 2015.

| Attributes     | Meaning                                                                                                                                                                                              |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id             | Unique ID for each home sold                                                                                                                                                                         |
| date           | Date of the home sale                                                                                                                                                                                |
| price          | Price of each home sold                                                                                                                                                                              |
| bedrooms       | Number of bedrooms                                                                                                                                                                                   |
| bathrooms      | Number of bathrooms, where .5 accounts for a room with a toilet but no shower                                                                                                                        |
| sqft_living    | Square footage of the apartments interior living space                                                                                                                                               |
| sqft_lot       | Square footage of the land space                                                                                                                                                                     |
| floors         | Number of floors                                                                                                                                                                                     |
| waterfront     | A dummy variable for whether the apartment was overlooking the waterfront or not                                                                                                                     |
| view           | An index from 0 to 4 of how good the view of the property was                                                                                                                                        |
| condition      | An index from 1 to 5 on the condition of the apartment                                                                                                                                               |
| grade          | An index from 1 to 13, where 1-3 falls short of building construction and design, 7 has an average level of construction and design, and 11-13 have a high quality level of construction and design. |
| sqft_above     | The square footage of the interior housing space that is above ground level                                                                                                                          |
| sqft_basement  | The square footage of the interior housing space that is below ground level                                                                                                                          |
| yr_built       | The year the house was initially built                                                                                                                                                               |
| yr_renovated   | The year of the house’s last renovation                                                                                                                                                              |
| zipcode        | What zipcode area the house is in                                                                                                                                                                    |
| lat            | Lattitude                                                                                                                                                                                            |
| long           | Longitude                                                                                                                                                                                            |
| sqft_living15  | The square footage of interior housing living space for the nearest 15 neighbors                                                                                                                     |
| sqft_lot15     | The square footage of the land lots of the nearest 15 neighbors                                                                                                                                      |

# Tools
<p align="left">
<a href="https://www.python.org/"> <img alt="Website img height="40" width="40" title="Python" src="https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/python.svg" /> </a>
<a href="https://jupyter.org/">  <img height="40" width="40" title="Jupyter" src="https://unpkg.com/simple-icons@6.0.0/icons/jupyter.svg" /> </a>
<a href="https://www.jetbrains.com/pycharm/">	 <img height="40" width="40" title="Pycharm" src="https://unpkg.com/simple-icons@6.0.0/icons/pycharm.svg" /> </a>
<a href="https://streamlit.io/">   <img height="40" width="40"  title="Streamlit" src="https://unpkg.com/simple-icons@5.24.0/icons/streamlit.svg" /> </a>
</p>


# Steps

- Data collection via Kaggle
- Business understanding
- Feature Engineering
- Transformation of variables
- Data cleaning
- Data exploration
- Project Deploy on Streamlit Cloud

# Business Hypotheses

|     | hypotheses                                                                     | Result | Business                                                             |
|-----|--------------------------------------------------------------------------------|--------|----------------------------------------------------------------------|
| h1  | More than 10% of Estates with waterfront are cheaper than average              | False  | Only ~6% of Estates with waterfront are cheaper than average.         |
| h2  | More than 60% of Estates with year built before 1955 are cheaper than average  | True   | Investing only on estates with condition >=3                         |
| h3  | Estates with basement have total area 40% bigger than estates without basement | False  | Investing in properties regardless of basement existence             |
| h4  | The estates growth price YoY (Year over Year) in 2015 is 10% in most regions   | True   | Investing in properties in the lower cost months     |
| h5  | The estates price growth MoM (Month over Month) between 2014-2015 is 20%       | False  | Investing in properties in the lower cost months                     |

# Conclusion
- Appealing properties for purchase have been grouped by location and season of the year. 
- Lots of good properties with year built below 1955 are available for 
purchase. 
- Although not a big number, some houses with waterfront are still viable to invest.
-  There are some vital months with good YoY/MoM variation that should have the necessary attention. 
-  The best time to sell properties is in Spring, as the price is higher at that time.
	
	
# Next steps
- Color adjustment for streamlit dark mode
- ML Algorithm implementation
	
# License

This project is under MIT License.

Done with ❤️ by João Renato Mendes 👋🏽 [Get in touch!](https://www.linkedin.com/in/joaorenatomendes/)

