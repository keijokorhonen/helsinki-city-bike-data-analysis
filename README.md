# helsinki-city-bike-data-analysis
Data analysis project on city bike usage patterns in the different districts of Helsinki in years 2017-2019

Group: Ville Marttila, Giulia Varvarà, Keijo Korhonen

We are investigating how city bikes, part of the Helsinki public transport system, are used in different districts of Helsinki. We do this by examining the directionality of bike rides to find directional patterns in the traffic flow between different districts at different times of the day and study how they correlate with demographic features of the districts. 
            
## Data: sources, wrangling, management        
            
City bike data:
https://www.hsl.fi/avoindata
This data set contains information on all city bike rides taken from 2016-2020, with their departure and arrival times and locations as well as their distance and time taken. There is bound to be some flawed data here, such as rides with a very short distance or time taken for a reason or another or rides starting and finishing at the same station within a short time (i.e. a person checking out a bike and returning it right away, possibly to exchange it to another one). The different attributes of the data points will be analysed in order to not only weed out the ones that do not represent valid bike rides and to discover and validate ones which do most likely represent real bike rides but have anomalies in some of their attributes due to sensor errors etc. (e.g. travel distance indicated as zero but departure and arrival locations being different).

Helsinki demographic data:
https://www.hel.fi/helsinki/en/administration/information/statistics/Databases/
https://hri.fi/data/en_GB/dataset/helsinki-vaesto
https://hri.fi/data/en_GB/dataset/helsinki-alueittain
This data set includes age, mother tongue, jobs, restaurants, students, etc. by district. 


## Data analysis: statistics, machine learning    

We first group up all city bike stations, based on their geographical location, into the different districts of Helsinki defined in the second data set.

Directionality could be studied in multiple ways. One could be to see directionality as an attribute of a district by calculating the differential between bike trips starting from and ending in the district. Another would be to compare the total travel distance (i.e. the "volume of travel") of rides out of the district to that of rides into the district. Yet another, which would look at bike travel as relationships between districts instead of properties of individual districts, would be to construct a two-dimensional matrix of starting and ending districts (with the time of day constituting a possible third dimension) and look at patterns of travel between different combinations of districts. In any of these cases the data could be grouped by the time of day, e.g. before and after noon or even in one-hour periods, and see how the directionality changes. (Residential districts will most likely have outwards directionality in the morning and inwards directionality in the evenings).

After defining the directionality of every district (or between pairs of districts) we can look at the correlation between different variables of the district data set. (e.g. number of jobs affects directionality during mornings and evenings, number of bars affects directionality in the night, etc.)


## Communication of results: summarization & visualization

Barplot: Districts vs total trips taken from and to district (directionality), Districts vs total distance of trips taken from and to district (directionality), each for the whole day, before and after noon

Scatter: Directionality vs jobs, directionality vs average income, directionality vs restaurants/bars, each for the whole day, before noon and after noon

Bubble Map: Bubbles in different districts with their size (and color) indicating directionality. The direction of the directionality can be expressed with an arrow instead of the bubble.

Flow Map: Arrows between different districts with either the size or color of the arrows indicating the traffic flow between the districts, either as an abstract map or superimposed on a geographical map of the districts.

            
## Operationalization: creating added value, end-user point of view

The data would help understand when and why city bikes are being used most frequently and could be used to explain the scarcity or excess of city bikes at stations during given periods. Studying the usage patterns of city bikes by different demographic features, such as whether income, degree of employment, number of students, or age distribution affects the usage patterns of bikes, could provide information that is useful in the planning of not only new city bike stations in new areas but also of the need for transportation of bikes between stations.

