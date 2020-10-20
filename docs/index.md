# A better and greener Helsinki through city bikes
## Modeling the expansion of the city bike system

Helsinki city bikes are being actively used throughout Helsinki and, working together with the Helsinki public transport network, have made personal transportation both more convenient and more environmentally friendly. While the majority of Helsinki residents have access to this convenient service, there are still some areas of Helsinki that are not yet covered by the Helsinki city bikes system. In order to aid in the planning for the expansion of the city bike network to cover the whole of Helsinki, we have created and trained a machine learning algorithm and to predict the most likely usage patterns of city bikes in districts currently outside the city bike network. This system will allow city planners to anticipate the needs of the new districts for new bike stations and bike transportation services, as well as the effects of adding new areas on existing areas of the city bike network through increased traffic to and from the new areas.

The current extent of the city bike system can be seen in the map below, with the districts containing bike stations in yellow and the districts currently outside the system in grey:
<div style="text-align: center;">
<iframe src="city_bike_network_noespoo.html"
    sandbox="allow-same-origin allow-scripts"
    width="616"
    height="634"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>
</div>

## What properties make a district use city bikes?
In order to predict the use of city bikes in new districts, our system considers both district demographics and existing bike usage patterns in the different districts of the city and uses these to construct a machine learning (ML) model that learns from the existing data on past usage patterns. There is good reason to believe that the demographic and geographic properties of different districts, such as distance from other districts, total population, unemployment rate, age distribution, number of restaurants and other amenities as well as the employment profile of them are good indicators of city bike usage. Our model makes use of a total of 63 different demographic variables per district as well as data on existing city bike usage differentiated by time of day, day of week and direction (into or out of the district). The demographic variables cover:

* total population and population density per km²
* age distribution
* average personal and median household income
* number of people on social assistance
* unemployment rate
* number of jobs by category
    * manufacturing, retail, transport, business, public
* number of jobs per km²
* number of buildings and total floor area by type
    * homes (houses and condominiums), business, public, industrial, other
* number of educational facilities
  * daycares, primary schools, middle schools, high schools, special schools
  * number of pupils or students on each level of education
* number of public facilities
  * libraries, health stations, playgrounds, swimming halls, sports halls, sports fields, churches, post offices, apothecaries, Alkos, grocery shops, other retail shops, restaurants, cafes and bars
* amount of natural facilities
  * natural forest and park areas in hectares, public beaches
* voting patterns
  * percentage voting SDP, KOK, VIHR, RKP, VAS, PS or other

## Describing city bike usage in the existing districts
Since the predictive machine learning model that we developed bases it predictions on historical data from thos districts that are currently within the city bike system, it is useful – and perhaps even crucial – for the evaluation of the predictions to have some kind of a baseline to compare to. For that purpose – and as a demonstration of what kind of data the model's training is based, we will first present some statistics from the existing city bike districts from the city bike season (a period of 214 days from April to October) of  2019. The following table presents the total number of rides departing from and ending in each of the districts with a percentage breakdown by the day of the week:

<table>
  <thead>
    <tr>
      <th>&nbsp;</th>
      <th colspan="2"><sub>Monday</sub></th>
      <th colspan="2"><sub>Tuesday</sub></th>
      <th colspan="2"><sub>Wednesday</sub></th>
      <th colspan="2"><sub>Thursday</sub></th>
      <th colspan="2"><sub>Friday</sub></th>
      <th colspan="2"><sub>Saturday</sub></th>
      <th colspan="2"><sub>Sunday</sub></th>
      <th colspan="2"><sub>Total</sub></th>
    </tr>  
    <tr>
      <th><sub>District</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th><sub>Vironniemi (101)</sub></th>
      <td><sub>15.3%</sub></td>
      <td><sub>15.5%</sub></td>
      <td><sub>16.2%</sub></td>
      <td><sub>16.2%</sub></td>
      <td><sub>17.0%</sub></td>
      <td><sub>17.0%</sub></td>
      <td><sub>16.1%</sub></td>
      <td><sub>16.0%</sub></td>
      <td><sub>14.8%</sub></td>
      <td><sub>14.3%</sub></td>
      <td><sub>11.6%</sub></td>
      <td><sub>11.3%</sub></td>
      <td><sub>9.2%</sub></td>
      <td><sub>9.8%</sub></td>
      <td><sub>421093</sub></td>
      <td><sub>413942</sub></td>
    </tr>
    <tr>
      <th><sub>Ullanlinna (102)</sub></th>
      <td><sub>14.0%</sub></td>
      <td><sub>14.1%</sub></td>
      <td><sub>15.1%</sub></td>
      <td><sub>15.0%</sub></td>
      <td><sub>16.8%</sub></td>
      <td><sub>16.7%</sub></td>
      <td><sub>15.6%</sub></td>
      <td><sub>15.5%</sub></td>
      <td><sub>14.2%</sub></td>
      <td><sub>14.0%</sub></td>
      <td><sub>13.7%</sub></td>
      <td><sub>13.7%</sub></td>
      <td><sub>10.6%</sub></td>
      <td><sub>11.0%</sub></td>
      <td><sub>282954</sub></td>
      <td><sub>271475</sub></td>
    </tr>
    <tr>
      <th><sub>Kampinmalmi (103)</sub></th>
      <td><sub>15.3%</sub></td>
      <td><sub>15.4%</sub></td>
      <td><sub>16.1%</sub></td>
      <td><sub>16.1%</sub></td>
      <td><sub>16.8%</sub></td>
      <td><sub>16.9%</sub></td>
      <td><sub>15.9%</sub></td>
      <td><sub>15.8%</sub></td>
      <td><sub>14.3%</sub></td>
      <td><sub>14.3%</sub></td>
      <td><sub>11.3%</sub></td>
      <td><sub>11.3%</sub></td>
      <td><sub>10.3%</sub></td>
      <td><sub>10.2%</sub></td>
      <td><sub>637419</sub></td>
      <td><sub>639288</sub></td>
    </tr>
    <tr>
      <th><sub>Taka-Töölö (104)</sub></th>
      <td><sub>14.4%</sub></td>
      <td><sub>14.1%</sub></td>
      <td><sub>15.3%</sub></td>
      <td><sub>15.4%</sub></td>
      <td><sub>16.1%</sub></td>
      <td><sub>16.1%</sub></td>
      <td><sub>15.5%</sub></td>
      <td><sub>15.5%</sub></td>
      <td><sub>13.8%</sub></td>
      <td><sub>14.0%</sub></td>
      <td><sub>12.9%</sub></td>
      <td><sub>13.1%</sub></td>
      <td><sub>12.0%</sub></td>
      <td><sub>11.8%</sub></td>
      <td><sub>191192</sub></td>
      <td><sub>190792</sub></td>
    </tr>
    <tr>
      <th><sub>Lauttasaari (105)</sub></th>
      <td><sub>15.2%</sub></td>
      <td><sub>14.9%</sub></td>
      <td><sub>15.6%</sub></td>
      <td><sub>15.6%</sub></td>
      <td><sub>16.5%</sub></td>
      <td><sub>16.5%</sub></td>
      <td><sub>15.8%</sub></td>
      <td><sub>15.9%</sub></td>
      <td><sub>13.8%</sub></td>
      <td><sub>14.2%</sub></td>
      <td><sub>11.7%</sub></td>
      <td><sub>12.1%</sub></td>
      <td><sub>11.4%</sub></td>
      <td><sub>10.8%</sub></td>
      <td><sub>128799</sub></td>
      <td><sub>129174</sub></td>
    </tr>
    <tr>
      <th><sub>Reijola (201)</sub></th>
      <td><sub>15.5%</sub></td>
      <td><sub>15.3%</sub></td>
      <td><sub>16.1%</sub></td>
      <td><sub>16.1%</sub></td>
      <td><sub>16.6%</sub></td>
      <td><sub>16.5%</sub></td>
      <td><sub>15.9%</sub></td>
      <td><sub>16.0%</sub></td>
      <td><sub>13.6%</sub></td>
      <td><sub>13.8%</sub></td>
      <td><sub>10.8%</sub></td>
      <td><sub>11.1%</sub></td>
      <td><sub>11.6%</sub></td>
      <td><sub>11.2%</sub></td>
      <td><sub>154524</sub></td>
      <td><sub>157072</sub></td>
    </tr>
    <tr>
      <th><sub>Munkkiniemi (202)</sub></th>
      <td><sub>14.4%</sub></td>
      <td><sub>14.2%</sub></td>
      <td><sub>15.2%</sub></td>
      <td><sub>15.1%</sub></td>
      <td><sub>15.7%</sub></td>
      <td><sub>15.6%</sub></td>
      <td><sub>15.1%</sub></td>
      <td><sub>14.9%</sub></td>
      <td><sub>13.3%</sub></td>
      <td><sub>13.5%</sub></td>
      <td><sub>12.9%</sub></td>
      <td><sub>13.6%</sub></td>
      <td><sub>13.3%</sub></td>
      <td><sub>13.0%</sub></td>
      <td><sub>79998</sub></td>
      <td><sub>75413</sub></td>
    </tr>
    <tr>
      <th><sub>Haaga (203)</sub></th>
      <td><sub>15.5%</sub></td>
      <td><sub>15.1%</sub></td>
      <td><sub>15.9%</sub></td>
      <td><sub>16.2%</sub></td>
      <td><sub>16.2%</sub></td>
      <td><sub>16.1%</sub></td>
      <td><sub>15.4%</sub></td>
      <td><sub>15.5%</sub></td>
      <td><sub>13.1%</sub></td>
      <td><sub>13.4%</sub></td>
      <td><sub>11.6%</sub></td>
      <td><sub>11.9%</sub></td>
      <td><sub>12.2%</sub></td>
      <td><sub>11.7%</sub></td>
      <td><sub>54305</sub></td>
      <td><sub>54163</sub></td>
    </tr>
    <tr>
      <th><sub>Pitäjänmäki (204)</sub></th>
      <td><sub>16.2%</sub></td>
      <td><sub>16.8%</sub></td>
      <td><sub>17.2%</sub></td>
      <td><sub>17.3%</sub></td>
      <td><sub>17.6%</sub></td>
      <td><sub>17.2%</sub></td>
      <td><sub>16.3%</sub></td>
      <td><sub>16.5%</sub></td>
      <td><sub>13.2%</sub></td>
      <td><sub>13.2%</sub></td>
      <td><sub>9.4%</sub></td>
      <td><sub>9.2%</sub></td>
      <td><sub>10.1%</sub></td>
      <td><sub>9.8%</sub></td>
      <td><sub>26023</sub></td>
      <td><sub>25212</sub></td>
    </tr>
    <tr>
      <th><sub>Kallio (301)</sub></th>
      <td><sub>14.4%</sub></td>
      <td><sub>14.4%</sub></td>
      <td><sub>15.7%</sub></td>
      <td><sub>15.7%</sub></td>
      <td><sub>16.3%</sub></td>
      <td><sub>16.3%</sub></td>
      <td><sub>15.6%</sub></td>
      <td><sub>15.7%</sub></td>
      <td><sub>14.1%</sub></td>
      <td><sub>13.8%</sub></td>
      <td><sub>13.0%</sub></td>
      <td><sub>12.9%</sub></td>
      <td><sub>10.8%</sub></td>
      <td><sub>11.2%</sub></td>
      <td><sub>301398</sub></td>
      <td><sub>296963</sub></td>
    </tr>
    <tr>
      <th><sub>Alppiharju (302)</sub></th>
      <td><sub>14.2%</sub></td>
      <td><sub>14.2%</sub></td>
      <td><sub>15.3%</sub></td>
      <td><sub>15.5%</sub></td>
      <td><sub>15.7%</sub></td>
      <td><sub>15.7%</sub></td>
      <td><sub>15.4%</sub></td>
      <td><sub>15.5%</sub></td>
      <td><sub>13.9%</sub></td>
      <td><sub>14.1%</sub></td>
      <td><sub>13.5%</sub></td>
      <td><sub>13.2%</sub></td>
      <td><sub>12.0%</sub></td>
      <td><sub>11.9%</sub></td>
      <td><sub>119889</sub></td>
      <td><sub>127831</sub></td>
    </tr>
    <tr>
      <th><sub>Vallila (303)</sub></th>
      <td><sub>15.7%</sub></td>
      <td><sub>15.5%</sub></td>
      <td><sub>16.6%</sub></td>
      <td><sub>16.5%</sub></td>
      <td><sub>16.8%</sub></td>
      <td><sub>16.6%</sub></td>
      <td><sub>16.2%</sub></td>
      <td><sub>16.3%</sub></td>
      <td><sub>13.9%</sub></td>
      <td><sub>14.4%</sub></td>
      <td><sub>10.3%</sub></td>
      <td><sub>10.4%</sub></td>
      <td><sub>10.6%</sub></td>
      <td><sub>10.3%</sub></td>
      <td><sub>160854</sub></td>
      <td><sub>172295</sub></td>
    </tr>
    <tr>
      <th><sub>Pasila (304)</sub></th>
      <td><sub>16.0%</sub></td>
      <td><sub>16.2%</sub></td>
      <td><sub>17.3%</sub></td>
      <td><sub>17.4%</sub></td>
      <td><sub>17.5%</sub></td>
      <td><sub>17.6%</sub></td>
      <td><sub>17.2%</sub></td>
      <td><sub>17.2%</sub></td>
      <td><sub>14.6%</sub></td>
      <td><sub>14.6%</sub></td>
      <td><sub>9.0%</sub></td>
      <td><sub>8.6%</sub></td>
      <td><sub>8.5%</sub></td>
      <td><sub>8.4%</sub></td>
      <td><sub>87883</sub></td>
      <td><sub>100909</sub></td>
    </tr>
    <tr>
      <th><sub>Vanhakaupunki (305)</sub></th>
      <td><sub>15.2%</sub></td>
      <td><sub>15.0%</sub></td>
      <td><sub>16.0%</sub></td>
      <td><sub>15.8%</sub></td>
      <td><sub>16.6%</sub></td>
      <td><sub>16.3%</sub></td>
      <td><sub>15.5%</sub></td>
      <td><sub>15.6%</sub></td>
      <td><sub>13.3%</sub></td>
      <td><sub>13.6%</sub></td>
      <td><sub>11.9%</sub></td>
      <td><sub>12.4%</sub></td>
      <td><sub>11.6%</sub></td>
      <td><sub>11.3%</sub></td>
      <td><sub>141257</sub></td>
      <td><sub>136675</sub></td>
    </tr>
    <tr>
      <th><sub>Maunula (401)</sub></th>
      <td><sub>15.9%</sub></td>
      <td><sub>15.6%</sub></td>
      <td><sub>15.0%</sub></td>
      <td><sub>14.7%</sub></td>
      <td><sub>15.7%</sub></td>
      <td><sub>15.5%</sub></td>
      <td><sub>14.3%</sub></td>
      <td><sub>15.1%</sub></td>
      <td><sub>12.6%</sub></td>
      <td><sub>12.8%</sub></td>
      <td><sub>12.8%</sub></td>
      <td><sub>12.6%</sub></td>
      <td><sub>13.7%</sub></td>
      <td><sub>13.7%</sub></td>
      <td><sub>6336</sub></td>
      <td><sub>6339</sub></td>
    </tr>
    <tr>
      <th><sub>Länsi-Pakila (402)</sub></th>
      <td><sub>14.1%</sub></td>
      <td><sub>14.0%</sub></td>
      <td><sub>13.9%</sub></td>
      <td><sub>13.7%</sub></td>
      <td><sub>15.4%</sub></td>
      <td><sub>13.8%</sub></td>
      <td><sub>14.1%</sub></td>
      <td><sub>13.0%</sub></td>
      <td><sub>12.6%</sub></td>
      <td><sub>13.9%</sub></td>
      <td><sub>14.0%</sub></td>
      <td><sub>14.7%</sub></td>
      <td><sub>15.9%</sub></td>
      <td><sub>17.0%</sub></td>
      <td><sub>2149</sub></td>
      <td><sub>1845</sub></td>
    </tr>
    <tr>
      <th><sub>Oulunkylä (404)</sub></th>
      <td><sub>15.1%</sub></td>
      <td><sub>15.2%</sub></td>
      <td><sub>15.2%</sub></td>
      <td><sub>15.3%</sub></td>
      <td><sub>15.8%</sub></td>
      <td><sub>16.0%</sub></td>
      <td><sub>15.7%</sub></td>
      <td><sub>15.6%</sub></td>
      <td><sub>13.4%</sub></td>
      <td><sub>13.5%</sub></td>
      <td><sub>12.2%</sub></td>
      <td><sub>12.1%</sub></td>
      <td><sub>12.6%</sub></td>
      <td><sub>12.4%</sub></td>
      <td><sub>26505</sub></td>
      <td><sub>26803</sub></td>
    </tr>
    <tr>
      <th><sub>Latokartano (501)</sub></th>
      <td><sub>15.6%</sub></td>
      <td><sub>14.7%</sub></td>
      <td><sub>15.6%</sub></td>
      <td><sub>15.3%</sub></td>
      <td><sub>15.8%</sub></td>
      <td><sub>15.4%</sub></td>
      <td><sub>14.8%</sub></td>
      <td><sub>14.5%</sub></td>
      <td><sub>12.7%</sub></td>
      <td><sub>12.9%</sub></td>
      <td><sub>12.2%</sub></td>
      <td><sub>13.7%</sub></td>
      <td><sub>13.2%</sub></td>
      <td><sub>13.6%</sub></td>
      <td><sub>32818</sub></td>
      <td><sub>30017</sub></td>
    </tr>
    <tr>
      <th><sub>Kulosaari (601)</sub></th>
      <td><sub>13.2%</sub></td>
      <td><sub>13.3%</sub></td>
      <td><sub>14.5%</sub></td>
      <td><sub>14.7%</sub></td>
      <td><sub>15.3%</sub></td>
      <td><sub>15.3%</sub></td>
      <td><sub>14.4%</sub></td>
      <td><sub>14.2%</sub></td>
      <td><sub>12.7%</sub></td>
      <td><sub>12.7%</sub></td>
      <td><sub>15.3%</sub></td>
      <td><sub>14.8%</sub></td>
      <td><sub>14.6%</sub></td>
      <td><sub>14.9%</sub></td>
      <td><sub>21965</sub></td>
      <td><sub>21870</sub></td>
    </tr>
    <tr>
      <th><sub>Herttoniemi (602)</sub></th>
      <td><sub>14.4%</sub></td>
      <td><sub>14.3%</sub></td>
      <td><sub>15.2%</sub></td>
      <td><sub>15.2%</sub></td>
      <td><sub>15.8%</sub></td>
      <td><sub>15.9%</sub></td>
      <td><sub>15.3%</sub></td>
      <td><sub>15.4%</sub></td>
      <td><sub>14.1%</sub></td>
      <td><sub>13.9%</sub></td>
      <td><sub>12.7%</sub></td>
      <td><sub>12.8%</sub></td>
      <td><sub>12.5%</sub></td>
      <td><sub>12.5%</sub></td>
      <td><sub>94502</sub></td>
      <td><sub>95385</sub></td>
    </tr>
    <tr>
      <th><sub>Laajasalo (603)</sub></th>
      <td><sub>14.1%</sub></td>
      <td><sub>13.8%</sub></td>
      <td><sub>13.8%</sub></td>
      <td><sub>13.5%</sub></td>
      <td><sub>13.6%</sub></td>
      <td><sub>14.1%</sub></td>
      <td><sub>14.1%</sub></td>
      <td><sub>14.1%</sub></td>
      <td><sub>11.9%</sub></td>
      <td><sub>12.5%</sub></td>
      <td><sub>15.6%</sub></td>
      <td><sub>16.0%</sub></td>
      <td><sub>16.8%</sub></td>
      <td><sub>16.0%</sub></td>
      <td><sub>12312</sub></td>
      <td><sub>11393</sub></td>
    </tr>
    <tr>
      <th><sub>Vartiokylä (701)</sub></th>
      <td><sub>14.5%</sub></td>
      <td><sub>14.6%</sub></td>
      <td><sub>15.1%</sub></td>
      <td><sub>15.1%</sub></td>
      <td><sub>15.6%</sub></td>
      <td><sub>15.6%</sub></td>
      <td><sub>15.1%</sub></td>
      <td><sub>15.0%</sub></td>
      <td><sub>14.4%</sub></td>
      <td><sub>14.4%</sub></td>
      <td><sub>13.2%</sub></td>
      <td><sub>13.4%</sub></td>
      <td><sub>12.0%</sub></td>
      <td><sub>12.0%</sub></td>
      <td><sub>42459</sub></td>
      <td><sub>41033</sub></td>
    </tr>
    <tr>
      <th><sub>Myllypuro (702)</sub></th>
      <td><sub>15.1%</sub></td>
      <td><sub>15.0%</sub></td>
      <td><sub>14.5%</sub></td>
      <td><sub>14.8%</sub></td>
      <td><sub>16.3%</sub></td>
      <td><sub>16.7%</sub></td>
      <td><sub>15.0%</sub></td>
      <td><sub>15.2%</sub></td>
      <td><sub>13.2%</sub></td>
      <td><sub>13.6%</sub></td>
      <td><sub>12.8%</sub></td>
      <td><sub>12.7%</sub></td>
      <td><sub>13.0%</sub></td>
      <td><sub>12.1%</sub></td>
      <td><sub>10194</sub></td>
      <td><sub>10939</sub></td>
    </tr>
  </tbody>
</table>

## Predicting city bike usage in new districts
Our machine learning algorithm provides predictions on the number of rides that are likely to be taken to and from different districts by modelling relationships between different districts at different points in time, which allows it to produce fine-grained data and take into account variations in usage patterns at different times of the day and different days of the week (also monthly or even weekly variation can be similarly taken into account if needed). This can reveal interesting and useful patterns in the usage profiles of different districts for both new and already covered areas and help in planning the maintenance and logistics of the city bike system. The following tables contain predictions for city bike traffic into and out of all the base districts currently outside the city bike system, generated by the machine learning model based on the abovementioned demographic data and existing bike usage patterns between all the current districts over the 2019 city bike season. The first table contains a prediction for the total number of city bike rides to and from each of the new areas, broken down into percentages by days of the week (with the total number of rides predicted for the entire season on the right):

 <table>
  <thead>
  <tr>
    <th>&nbsp;</th>
    <th colspan="2"><sub>Monday</sub></th>
    <th colspan="2"><sub>Tuesday</sub></th>
    <th colspan="2"><sub>Wednesday</sub></th>
    <th colspan="2"><sub>Thursday</sub></th>
    <th colspan="2"><sub>Friday</sub></th>
    <th colspan="2"><sub>Saturday</sub></th>
    <th colspan="2"><sub>Sunday</sub></th>
    <th colspan="2"><sub>Total</sub></th>
  </tr>  
  <tr>
      <th><sub>District</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th><sub>Kaarela (205)</sub></th>
      <td><sub>15.6%</sub></td>
      <td><sub>16.0%</sub></td>
      <td><sub>16.2%</sub></td>
      <td><sub>16.3%</sub></td>
      <td><sub>16.5%</sub></td>
      <td><sub>16.5%</sub></td>
      <td><sub>16.2%</sub></td>
      <td><sub>15.6%</sub></td>
      <td><sub>13.3%</sub></td>
      <td><sub>13.5%</sub></td>
      <td><sub>11.2%</sub></td>
      <td><sub>11.6%</sub></td>
      <td><sub>11.0%</sub></td>
      <td><sub>10.6%</sub></td>
      <td><sub>25064</sub></td>
      <td><sub>25741</sub></td>
    </tr>
    <tr>
      <th><sub>Tuomarinkylä (403)</sub></th>
      <td><sub>14.7%</sub></td>
      <td><sub>16.3%</sub></td>
      <td><sub>15.5%</sub></td>
      <td><sub>15.5%</sub></td>
      <td><sub>17.3%</sub></td>
      <td><sub>16.7%</sub></td>
      <td><sub>14.8%</sub></td>
      <td><sub>15.1%</sub></td>
      <td><sub>14.0%</sub></td>
      <td><sub>12.3%</sub></td>
      <td><sub>12.1%</sub></td>
      <td><sub>12.8%</sub></td>
      <td><sub>11.4%</sub></td>
      <td><sub>11.2%</sub></td>
      <td><sub>17658</sub></td>
      <td><sub>16472</sub></td>
    </tr>
    <tr>
      <th><sub>Itä-Pakila (405)</sub></th>
      <td><sub>15.4%</sub></td>
      <td><sub>16.2%</sub></td>
      <td><sub>15.4%</sub></td>
      <td><sub>16.0%</sub></td>
      <td><sub>15.7%</sub></td>
      <td><sub>16.1%</sub></td>
      <td><sub>14.3%</sub></td>
      <td><sub>14.8%</sub></td>
      <td><sub>13.7%</sub></td>
      <td><sub>12.8%</sub></td>
      <td><sub>13.2%</sub></td>
      <td><sub>12.6%</sub></td>
      <td><sub>12.2%</sub></td>
      <td><sub>11.5%</sub></td>
      <td><sub>20706</sub></td>
      <td><sub>20586</sub></td>
    </tr>
    <tr>
      <th><sub>Pukinmäki (502)</sub></th>
      <td><sub>15.6%</sub></td>
      <td><sub>16.2%</sub></td>
      <td><sub>16.1%</sub></td>
      <td><sub>15.7%</sub></td>
      <td><sub>15.8%</sub></td>
      <td><sub>16.7%</sub></td>
      <td><sub>15.9%</sub></td>
      <td><sub>15.7%</sub></td>
      <td><sub>13.9%</sub></td>
      <td><sub>13.9%</sub></td>
      <td><sub>11.4%</sub></td>
      <td><sub>11.4%</sub></td>
      <td><sub>11.2%</sub></td>
      <td><sub>10.3%</sub></td>
      <td><sub>22770</sub></td>
      <td><sub>22998</sub></td>
    </tr>
    <tr>
      <th><sub>Malmi (503)</sub></th>
      <td><sub>15.9%</sub></td>
      <td><sub>15.5%</sub></td>
      <td><sub>16.1%</sub></td>
      <td><sub>15.2%</sub></td>
      <td><sub>17.8%</sub></td>
      <td><sub>15.9%</sub></td>
      <td><sub>17.1%</sub></td>
      <td><sub>15.9%</sub></td>
      <td><sub>11.6%</sub></td>
      <td><sub>14.6%</sub></td>
      <td><sub>10.8%</sub></td>
      <td><sub>11.7%</sub></td>
      <td><sub>10.6%</sub></td>
      <td><sub>11.2%</sub></td>
      <td><sub>18954</sub></td>
      <td><sub>17429</sub></td>
    </tr>
    <tr>
      <th><sub>Suutarila (504)</sub></th>
      <td><sub>15.6%</sub></td>
      <td><sub>15.4%</sub></td>
      <td><sub>16.2%</sub></td>
      <td><sub>15.4%</sub></td>
      <td><sub>15.7%</sub></td>
      <td><sub>17.1%</sub></td>
      <td><sub>16.2%</sub></td>
      <td><sub>15.4%</sub></td>
      <td><sub>12.6%</sub></td>
      <td><sub>13.0%</sub></td>
      <td><sub>11.7%</sub></td>
      <td><sub>12.4%</sub></td>
      <td><sub>12.1%</sub></td>
      <td><sub>11.3%</sub></td>
      <td><sub>9151</sub></td>
      <td><sub>9127</sub></td>
    </tr>
    <tr>
      <th><sub>Puistola (505)</sub></th>
      <td><sub>16.0%</sub></td>
      <td><sub>16.2%</sub></td>
      <td><sub>16.2%</sub></td>
      <td><sub>15.7%</sub></td>
      <td><sub>16.4%</sub></td>
      <td><sub>16.4%</sub></td>
      <td><sub>15.1%</sub></td>
      <td><sub>15.4%</sub></td>
      <td><sub>12.3%</sub></td>
      <td><sub>13.3%</sub></td>
      <td><sub>11.5%</sub></td>
      <td><sub>12.0%</sub></td>
      <td><sub>12.4%</sub></td>
      <td><sub>11.0%</sub></td>
      <td><sub>9338</sub></td>
      <td><sub>9297</sub></td>
    </tr>
    <tr>
      <th><sub>Jakomäki (506)</sub></th>
      <td><sub>15.8%</sub></td>
      <td><sub>16.1%</sub></td>
      <td><sub>16.5%</sub></td>
      <td><sub>15.8%</sub></td>
      <td><sub>16.1%</sub></td>
      <td><sub>16.9%</sub></td>
      <td><sub>16.2%</sub></td>
      <td><sub>15.3%</sub></td>
      <td><sub>12.9%</sub></td>
      <td><sub>13.5%</sub></td>
      <td><sub>11.2%</sub></td>
      <td><sub>11.7%</sub></td>
      <td><sub>11.2%</sub></td>
      <td><sub>10.6%</sub></td>
      <td><sub>10992</sub></td>
      <td><sub>10645</sub></td>
    </tr>
    <tr>
      <th><sub>Mellunkylä (703)</sub></th>
      <td><sub>13.6%</sub></td>
      <td><sub>15.0%</sub></td>
      <td><sub>17.4%</sub></td>
      <td><sub>17.7%</sub></td>
      <td><sub>17.1%</sub></td>
      <td><sub>19.5%</sub></td>
      <td><sub>15.7%</sub></td>
      <td><sub>15.5%</sub></td>
      <td><sub>13.3%</sub></td>
      <td><sub>12.9%</sub></td>
      <td><sub>11.3%</sub></td>
      <td><sub>10.3%</sub></td>
      <td><sub>11.7%</sub></td>
      <td><sub>9.2%</sub></td>
      <td><sub>28528</sub></td>
      <td><sub>32181</sub></td>
    </tr>
    <tr>
      <th><sub>Vuosaari (704)</sub></th>
      <td><sub>12.7%</sub></td>
      <td><sub>14.6%</sub></td>
      <td><sub>17.0%</sub></td>
      <td><sub>18.7%</sub></td>
      <td><sub>19.5%</sub></td>
      <td><sub>20.6%</sub></td>
      <td><sub>15.2%</sub></td>
      <td><sub>15.4%</sub></td>
      <td><sub>13.8%</sub></td>
      <td><sub>12.5%</sub></td>
      <td><sub>10.6%</sub></td>
      <td><sub>9.2%</sub></td>
      <td><sub>11.2%</sub></td>
      <td><sub>8.9%</sub></td>
      <td><sub>22246</sub></td>
      <td><sub>26241</sub></td>
    </tr>
    <tr>
      <th><sub>Östersundom (801)</sub></th>
      <td><sub>15.4%</sub></td>
      <td><sub>15.0%</sub></td>
      <td><sub>14.8%</sub></td>
      <td><sub>13.4%</sub></td>
      <td><sub>17.1%</sub></td>
      <td><sub>16.4%</sub></td>
      <td><sub>12.8%</sub></td>
      <td><sub>15.5%</sub></td>
      <td><sub>12.8%</sub></td>
      <td><sub>13.4%</sub></td>
      <td><sub>13.8%</sub></td>
      <td><sub>13.7%</sub></td>
      <td><sub>13.4%</sub></td>
      <td><sub>12.7%</sub></td>
      <td><sub>18044</sub></td>
      <td><sub>17689</sub></td>
    </tr>
  </tbody>
</table>

The following table presents the same data on the total number of rides predicted over the entire season, this time broken down to percentages by the time of day to demonstrate the differences in the daily distribution of traffic in and out of the different districts:

<table>
  <thead>
    <tr>
      <th>&nbsp;</th>
      <th colspan="2"><sub>Morning</sub></th>
      <th colspan="2"><sub>Day</sub></th>
      <th colspan="2"><sub>Evening</sub></th>
      <th colspan="2"><sub>Night</sub></th>
      <th colspan="2"><sub>Total</sub></th>
    </tr>  
    <tr>
      <th><sub>District</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th><sub>Kaarela (205)</sub></th>
      <td><sub>24.1%</sub></td>
      <td><sub>25.4%</sub></td>
      <td><sub>43.0%</sub></td>
      <td><sub>44.7%</sub></td>
      <td><sub>28.6%</sub></td>
      <td><sub>26.0%</sub></td>
      <td><sub>4.3%</sub></td>
      <td><sub>3.9%</sub></td>
      <td><sub>25064</sub></td>
      <td><sub>25741</sub></td>
    </tr>
    <tr>
      <th><sub>Tuomarinkylä (403)</sub></th>
      <td><sub>21.2%</sub></td>
      <td><sub>25.7%</sub></td>
      <td><sub>44.9%</sub></td>
      <td><sub>43.0%</sub></td>
      <td><sub>28.6%</sub></td>
      <td><sub>27.5%</sub></td>
      <td><sub>5.2%</sub></td>
      <td><sub>3.9%</sub></td>
      <td><sub>17658</sub></td>
      <td><sub>16472</sub></td>
    </tr>
    <tr>
      <th><sub>Itä-Pakila (405)</sub></th>
      <td><sub>19.2%</sub></td>
      <td><sub>24.5%</sub></td>
      <td><sub>44.4%</sub></td>
      <td><sub>42.2%</sub></td>
      <td><sub>31.2%</sub></td>
      <td><sub>29.4%</sub></td>
      <td><sub>5.1%</sub></td>
      <td><sub>3.9%</sub></td>
      <td><sub>20706</sub></td>
      <td><sub>20586</sub></td>
    </tr>
    <tr>
      <th><sub>Pukinmäki (502)</sub></th>
      <td><sub>22.7%</sub></td>
      <td><sub>25.6%</sub></td>
      <td><sub>42.7%</sub></td>
      <td><sub>44.3%</sub></td>
      <td><sub>29.7%</sub></td>
      <td><sub>25.8%</sub></td>
      <td><sub>4.9%</sub></td>
      <td><sub>4.2%</sub></td>
      <td><sub>22770</sub></td>
      <td><sub>22998</sub></td>
    </tr>
    <tr>
      <th><sub>Malmi (503)</sub></th>
      <td><sub>23.9%</sub></td>
      <td><sub>27.0%</sub></td>
      <td><sub>40.5%</sub></td>
      <td><sub>41.8%</sub></td>
      <td><sub>29.9%</sub></td>
      <td><sub>26.9%</sub></td>
      <td><sub>5.7%</sub></td>
      <td><sub>4.2%</sub></td>
      <td><sub>18954</sub></td>
      <td><sub>17429</sub></td>
    </tr>
    <tr>
      <th><sub>Suutarila (504)</sub></th>
      <td><sub>16.9%</sub></td>
      <td><sub>29.3%</sub></td>
      <td><sub>44.8%</sub></td>
      <td><sub>40.9%</sub></td>
      <td><sub>31.7%</sub></td>
      <td><sub>25.9%</sub></td>
      <td><sub>6.4%</sub></td>
      <td><sub>3.9%</sub></td>
      <td><sub>9151</sub></td>
      <td><sub>9127</sub></td>
    </tr>
    <tr>
      <th><sub>Puistola (505)</sub></th>
      <td><sub>17.5%</sub></td>
      <td><sub>27.0%</sub></td>
      <td><sub>44.4%</sub></td>
      <td><sub>42.8%</sub></td>
      <td><sub>32.0%</sub></td>
      <td><sub>26.5%</sub></td>
      <td><sub>6.1%</sub></td>
      <td><sub>3.7%</sub></td>
      <td><sub>9338</sub></td>
      <td><sub>9297</sub></td>
    </tr>
    <tr>
      <th><sub>Jakomäki (506)</sub></th>
      <td><sub>18.4%</sub></td>
      <td><sub>29.2%</sub></td>
      <td><sub>43.5%</sub></td>
      <td><sub>41.9%</sub></td>
      <td><sub>32.4%</sub></td>
      <td><sub>25.0%</sub></td>
      <td><sub>5.7%</sub></td>
      <td><sub>4.0%</sub></td>
      <td><sub>10992</sub></td>
      <td><sub>10645</sub></td>
    </tr>
    <tr>
      <th><sub>Mellunkylä (703)</sub></th>
      <td><sub>18.9%</sub></td>
      <td><sub>30.2%</sub></td>
      <td><sub>46.3%</sub></td>
      <td><sub>43.8%</sub></td>
      <td><sub>28.9%</sub></td>
      <td><sub>21.8%</sub></td>
      <td><sub>5.9%</sub></td>
      <td><sub>4.2%</sub></td>
      <td><sub>28528</sub></td>
      <td><sub>32181</sub></td>
    </tr>
    <tr>
      <th><sub>Vuosaari (704)</sub></th>
      <td><sub>17.2%</sub></td>
      <td><sub>32.8%</sub></td>
      <td><sub>49.1%</sub></td>
      <td><sub>43.3%</sub></td>
      <td><sub>27.4%</sub></td>
      <td><sub>20.6%</sub></td>
      <td><sub>6.3%</sub></td>
      <td><sub>3.3%</sub></td>
      <td><sub>22246</sub></td>
      <td><sub>26241</sub></td>
    </tr>
    <tr>
      <th><sub>Östersundom (801)</sub></th>
      <td><sub>22.3%</sub></td>
      <td><sub>18.7%</sub></td>
      <td><sub>43.8%</sub></td>
      <td><sub>39.9%</sub></td>
      <td><sub>28.5%</sub></td>
      <td><sub>36.9%</sub></td>
      <td><sub>5.4%</sub></td>
      <td><sub>4.4%</sub></td>
      <td><sub>18044</sub></td>
      <td><sub>17689</sub></td>
    </tr>
  </tbody>
</table>

Since the percentages of the total numbers over the whole season are not necessarily the most informative presentation, the following table gives the same information as a more concrete average number of rides per day of the week, the total representing the average number of rides to and from the district during one week over the entire season: 

<table>
  <thead>
    <tr>
      <th>&nbsp;</th>
      <th colspan="2"><sub>Monday</sub></th>
      <th colspan="2"><sub>Tuesday</sub></th>
      <th colspan="2"><sub>Wednesday</sub></th>
      <th colspan="2"><sub>Thursday</sub></th>
      <th colspan="2"><sub>Friday</sub></th>
      <th colspan="2"><sub>Saturday</sub></th>
      <th colspan="2"><sub>Sunday</sub></th>
      <th colspan="2"><sub>Total</sub></th>
    </tr>  
    <tr>
      <th><sub>District</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th><sub>Kaarela (205)</sub></th>
      <td><sub>128</sub></td>
      <td><sub>134</sub></td>
      <td><sub>132</sub></td>
      <td><sub>136</sub></td>
      <td><sub>134</sub></td>
      <td><sub>138</sub></td>
      <td><sub>133</sub></td>
      <td><sub>131</sub></td>
      <td><sub>108</sub></td>
      <td><sub>113</sub></td>
      <td><sub>91</sub></td>
      <td><sub>97</sub></td>
      <td><sub>90</sub></td>
      <td><sub>89</sub></td>
      <td><sub>819</sub></td>
      <td><sub>842</sub></td>
    </tr>
    <tr>
      <th><sub>Tuomarinkylä (403)</sub></th>
      <td><sub>85</sub></td>
      <td><sub>87</sub></td>
      <td><sub>89</sub></td>
      <td><sub>83</sub></td>
      <td><sub>100</sub></td>
      <td><sub>90</sub></td>
      <td><sub>85</sub></td>
      <td><sub>81</sub></td>
      <td><sub>81</sub></td>
      <td><sub>66</sub></td>
      <td><sub>70</sub></td>
      <td><sub>69</sub></td>
      <td><sub>65</sub></td>
      <td><sub>60</sub></td>
      <td><sub>577</sub></td>
      <td><sub>538</sub></td>
    </tr>
    <tr>
      <th><sub>Itä-Pakila (405)</sub></th>
      <td><sub>104</sub></td>
      <td><sub>109</sub></td>
      <td><sub>104</sub></td>
      <td><sub>107</sub></td>
      <td><sub>106</sub></td>
      <td><sub>108</sub></td>
      <td><sub>97</sub></td>
      <td><sub>100</sub></td>
      <td><sub>92</sub></td>
      <td><sub>86</sub></td>
      <td><sub>89</sub></td>
      <td><sub>84</sub></td>
      <td><sub>82</sub></td>
      <td><sub>77</sub></td>
      <td><sub>677</sub></td>
      <td><sub>673</sub></td>
    </tr>
    <tr>
      <th><sub>Pukinmäki (502)</sub></th>
      <td><sub>116</sub></td>
      <td><sub>122</sub></td>
      <td><sub>119</sub></td>
      <td><sub>118</sub></td>
      <td><sub>117</sub></td>
      <td><sub>125</sub></td>
      <td><sub>118</sub></td>
      <td><sub>118</sub></td>
      <td><sub>103</sub></td>
      <td><sub>104</sub></td>
      <td><sub>85</sub></td>
      <td><sub>85</sub></td>
      <td><sub>83</sub></td>
      <td><sub>77</sub></td>
      <td><sub>744</sub></td>
      <td><sub>752</sub></td>
    </tr>
    <tr>
      <th><sub>Malmi (503)</sub></th>
      <td><sub>98</sub></td>
      <td><sub>88</sub></td>
      <td><sub>99</sub></td>
      <td><sub>86</sub></td>
      <td><sub>110</sub></td>
      <td><sub>90</sub></td>
      <td><sub>106</sub></td>
      <td><sub>90</sub></td>
      <td><sub>71</sub></td>
      <td><sub>83</sub></td>
      <td><sub>66</sub></td>
      <td><sub>66</sub></td>
      <td><sub>65</sub></td>
      <td><sub>63</sub></td>
      <td><sub>620</sub></td>
      <td><sub>570</sub></td>
    </tr>
    <tr>
      <th><sub>Suutarila (504)</sub></th>
      <td><sub>46</sub></td>
      <td><sub>46</sub></td>
      <td><sub>48</sub></td>
      <td><sub>45</sub></td>
      <td><sub>47</sub></td>
      <td><sub>50</sub></td>
      <td><sub>48</sub></td>
      <td><sub>45</sub></td>
      <td><sub>37</sub></td>
      <td><sub>38</sub></td>
      <td><sub>34</sub></td>
      <td><sub>37</sub></td>
      <td><sub>36</sub></td>
      <td><sub>33</sub></td>
      <td><sub>299</sub></td>
      <td><sub>298</sub></td>
    </tr>
    <tr>
      <th><sub>Puistola (505)</sub></th>
      <td><sub>49</sub></td>
      <td><sub>49</sub></td>
      <td><sub>49</sub></td>
      <td><sub>47</sub></td>
      <td><sub>49</sub></td>
      <td><sub>49</sub></td>
      <td><sub>46</sub></td>
      <td><sub>46</sub></td>
      <td><sub>37</sub></td>
      <td><sub>40</sub></td>
      <td><sub>35</sub></td>
      <td><sub>36</sub></td>
      <td><sub>37</sub></td>
      <td><sub>33</sub></td>
      <td><sub>305</sub></td>
      <td><sub>304</sub></td>
    </tr>
    <tr>
      <th><sub>Jakomäki (506)</sub></th>
      <td><sub>56</sub></td>
      <td><sub>56</sub></td>
      <td><sub>59</sub></td>
      <td><sub>55</sub></td>
      <td><sub>57</sub></td>
      <td><sub>58</sub></td>
      <td><sub>58</sub></td>
      <td><sub>53</sub></td>
      <td><sub>46</sub></td>
      <td><sub>47</sub></td>
      <td><sub>40</sub></td>
      <td><sub>40</sub></td>
      <td><sub>40</sub></td>
      <td><sub>37</sub></td>
      <td><sub>359</sub></td>
      <td><sub>348</sub></td>
    </tr>
    <tr>
      <th><sub>Mellunkylä (703)</sub></th>
      <td><sub>126</sub></td>
      <td><sub>157</sub></td>
      <td><sub>162</sub></td>
      <td><sub>186</sub></td>
      <td><sub>159</sub></td>
      <td><sub>204</sub></td>
      <td><sub>146</sub></td>
      <td><sub>163</sub></td>
      <td><sub>123</sub></td>
      <td><sub>135</sub></td>
      <td><sub>105</sub></td>
      <td><sub>108</sub></td>
      <td><sub>108</sub></td>
      <td><sub>96</sub></td>
      <td><sub>933</sub></td>
      <td><sub>1052</sub></td>
    </tr>
    <tr>
      <th><sub>Vuosaari (704)</sub></th>
      <td><sub>92</sub></td>
      <td><sub>125</sub></td>
      <td><sub>123</sub></td>
      <td><sub>160</sub></td>
      <td><sub>141</sub></td>
      <td><sub>176</sub></td>
      <td><sub>110</sub></td>
      <td><sub>132</sub></td>
      <td><sub>100</sub></td>
      <td><sub>107</sub></td>
      <td><sub>77</sub></td>
      <td><sub>78</sub></td>
      <td><sub>81</sub></td>
      <td><sub>76</sub></td>
      <td><sub>727</sub></td>
      <td><sub>858</sub></td>
    </tr>
    <tr>
      <th><sub>Östersundom (801)</sub></th>
      <td><sub>90</sub></td>
      <td><sub>86</sub></td>
      <td><sub>87</sub></td>
      <td><sub>77</sub></td>
      <td><sub>100</sub></td>
      <td><sub>94</sub></td>
      <td><sub>75</sub></td>
      <td><sub>89</sub></td>
      <td><sub>75</sub></td>
      <td><sub>77</sub></td>
      <td><sub>81</sub></td>
      <td><sub>78</sub></td>
      <td><sub>78</sub></td>
      <td><sub>73</sub></td>
      <td><sub>590</sub></td>
      <td><sub>578</sub></td>
    </tr>
  </tbody>
</table>

Finally, the fourth table presents the same information split down even further into the average number of rides during different periods of the day, the total here representing the average number of rides taken to and from the district over a single day:

<table>
  <thead>
    <tr>
      <th>&nbsp;</th>
      <th colspan="2"><sub>Morning</sub></th>
      <th colspan="2"><sub>Day</sub></th>
      <th colspan="2"><sub>Evening</sub></th>
      <th colspan="2"><sub>Night</sub></th>
      <th colspan="2"><sub>Total</sub></th>
    </tr>  
    <tr>
      <th><sub>District</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
      <th><sub>In</sub></th>
      <th><sub>Out</sub></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th><sub>Kaarela (205)</sub></th>
      <td><sub>28</sub></td>
      <td><sub>30</sub></td>
      <td><sub>50</sub></td>
      <td><sub>53</sub></td>
      <td><sub>33</sub></td>
      <td><sub>31</sub></td>
      <td><sub>5</sub></td>
      <td><sub>4</sub></td>
      <td><sub>117</sub></td>
      <td><sub>120</sub></td>
    </tr>
    <tr>
      <th><sub>Tuomarinkylä (403)</sub></th>
      <td><sub>17</sub></td>
      <td><sub>19</sub></td>
      <td><sub>37</sub></td>
      <td><sub>33</sub></td>
      <td><sub>23</sub></td>
      <td><sub>21</sub></td>
      <td><sub>4</sub></td>
      <td><sub>2</sub></td>
      <td><sub>82</sub></td>
      <td><sub>76</sub></td>
    </tr>
    <tr>
      <th><sub>Itä-Pakila (405)</sub></th>
      <td><sub>18</sub></td>
      <td><sub>23</sub></td>
      <td><sub>42</sub></td>
      <td><sub>40</sub></td>
      <td><sub>30</sub></td>
      <td><sub>28</sub></td>
      <td><sub>4</sub></td>
      <td><sub>3</sub></td>
      <td><sub>96</sub></td>
      <td><sub>96</sub></td>
    </tr>
    <tr>
      <th><sub>Pukinmäki (502)</sub></th>
      <td><sub>24</sub></td>
      <td><sub>27</sub></td>
      <td><sub>45</sub></td>
      <td><sub>47</sub></td>
      <td><sub>31</sub></td>
      <td><sub>27</sub></td>
      <td><sub>5</sub></td>
      <td><sub>4</sub></td>
      <td><sub>106</sub></td>
      <td><sub>107</sub></td>
    </tr>
    <tr>
      <th><sub>Malmi (503)</sub></th>
      <td><sub>21</sub></td>
      <td><sub>21</sub></td>
      <td><sub>35</sub></td>
      <td><sub>34</sub></td>
      <td><sub>26</sub></td>
      <td><sub>21</sub></td>
      <td><sub>5</sub></td>
      <td><sub>3</sub></td>
      <td><sub>88</sub></td>
      <td><sub>81</sub></td>
    </tr>
    <tr>
      <th><sub>Suutarila (504)</sub></th>
      <td><sub>7</sub></td>
      <td><sub>12</sub></td>
      <td><sub>19</sub></td>
      <td><sub>17</sub></td>
      <td><sub>13</sub></td>
      <td><sub>11</sub></td>
      <td><sub>2</sub></td>
      <td><sub>1</sub></td>
      <td><sub>42</sub></td>
      <td><sub>42</sub></td>
    </tr>
    <tr>
      <th><sub>Puistola (505)</sub></th>
      <td><sub>7</sub></td>
      <td><sub>11</sub></td>
      <td><sub>19</sub></td>
      <td><sub>18</sub></td>
      <td><sub>13</sub></td>
      <td><sub>11</sub></td>
      <td><sub>2</sub></td>
      <td><sub>1</sub></td>
      <td><sub>43</sub></td>
      <td><sub>43</sub></td>
    </tr>
    <tr>
      <th><sub>Jakomäki (506)</sub></th>
      <td><sub>9</sub></td>
      <td><sub>14</sub></td>
      <td><sub>22</sub></td>
      <td><sub>20</sub></td>
      <td><sub>16</sub></td>
      <td><sub>12</sub></td>
      <td><sub>2</sub></td>
      <td><sub>1</sub></td>
      <td><sub>51</sub></td>
      <td><sub>49</sub></td>
    </tr>
    <tr>
      <th><sub>Mellunkylä (703)</sub></th>
      <td><sub>25</sub></td>
      <td><sub>45</sub></td>
      <td><sub>61</sub></td>
      <td><sub>65</sub></td>
      <td><sub>38</sub></td>
      <td><sub>32</sub></td>
      <td><sub>7</sub></td>
      <td><sub>6</sub></td>
      <td><sub>133</sub></td>
      <td><sub>150</sub></td>
    </tr>
    <tr>
      <th><sub>Vuosaari (704)</sub></th>
      <td><sub>17</sub></td>
      <td><sub>40</sub></td>
      <td><sub>51</sub></td>
      <td><sub>53</sub></td>
      <td><sub>28</sub></td>
      <td><sub>25</sub></td>
      <td><sub>6</sub></td>
      <td><sub>4</sub></td>
      <td><sub>103</sub></td>
      <td><sub>122</sub></td>
    </tr>
    <tr>
      <th><sub>Östersundom (801)</sub></th>
      <td><sub>18</sub></td>
      <td><sub>15</sub></td>
      <td><sub>36</sub></td>
      <td><sub>33</sub></td>
      <td><sub>24</sub></td>
      <td><sub>30</sub></td>
      <td><sub>4</sub></td>
      <td><sub>3</sub></td>
      <td><sub>84</sub></td>
      <td><sub>82</sub></td>
    </tr>
  </tbody>
</table>

## Wider effects of expanding the city bike system

In addition to being subdivided along different temporal dimensions, the data used and the predictions produced by our system is also quite detailed in the spatial dimension, in that the system calculates the predictions on the level of individual pairs of districts. This means that in addition to the aggregate data displayed above, it also produces detailed predictions on the sources and destinations of the rides taken from a new district added to the system, providing the predicted numbers of rides taken to and from all the existing districts in the system. This is important not just in terms of predicting the usage patterns of the new districts, but also in terms of predicting the effects that adding new districts to the system has on the *existing* areas. Since the expansion of the city bike network involves adding new bike stations (and bikes) to new areas with new potential users, it will by default result in an increase in overall traffic. Since these new users are unlikely to travel only within their own district – and users from other districts can also be expected to occasionally visit these districts – this means that the addition of new districts is likely to generate new traffic also to and from the existing districts. 

The prediction data produced by the system can conveniently be also used to predict changes in the traffic of the existing areas. The following plots display, in visual form, the effects of adding each of the seven new districts directly bordering the existing city bike area (these districts are the most likely targets for expansion and will need to be added before the areas beyond them). The colour – progressing from light to dark blue with increasing traffic – indicates the predicted new traffic either from the coloured districts to the new districts ('Incoming') or from the new district to the coloured districts ('Outgoing'). The info box that can be seen by hovering the cursor over the area shows the number of average daily rides to or from that district from or to the added new district (shown in black).

### Kaarela
<div style="text-align: center;">
<iframe src="plots/Kaarela.html"
    sandbox="allow-same-origin allow-scripts"
    width="616"
    height="634"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>
</div>

### Tuomarinkylä
<div style="text-align: center;">
<iframe src="plots/Tuomarinkyla.html"
    sandbox="allow-same-origin allow-scripts"
    width="616"
    height="634"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>
</div>

### Itä-Pakila
<div style="text-align: center;">
<iframe src="plots/Ita-Pakila.html"
    sandbox="allow-same-origin allow-scripts"
    width="616"
    height="634"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>
</div>

### Pukinmäki
<div style="text-align: center;">
<iframe src="plots/Pukinmaki.html"
    sandbox="allow-same-origin allow-scripts"
    width="616"
    height="634"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>
</div>

### Malmi
<div style="text-align: center;">
<iframe src="plots/Malmi.html"
    sandbox="allow-same-origin allow-scripts"
    width="616"
    height="634"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>
</div>

### Mellunkylä
<div style="text-align: center;">
<iframe src="plots/Mellunkyla.html"
    sandbox="allow-same-origin allow-scripts"
    width="616"
    height="634"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>
</div>

### Vuosaari
<div style="text-align: center;">
<iframe src="plots/Vuosaari.html"
    sandbox="allow-same-origin allow-scripts"
    width="616"
    height="634"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>
</div>

## Some thoughts on the results

There are several ways to interpret the results produced by the machine learning prediction algorithm, however let us discuss them in terms of its temporal and geographical distributions. In terms of temporal distribution, the prediction clearly indicates that city bikes would most likely be used for work or other practical travel, since all districts apart from Östersundom – which can quite literally be considered something of an outlier – show less rides on weekends than on weekdays, and the majority of rides seem to be predicted for the day as opposed to the morning or evening – the night quite expectedly having only a small minority of rides.

In terms of geographical distribution, spatial proximity seemed to be – rather unsurprisingly – the strongest single predictor of bike rides between districts, but as can be seen from the plots, it is clearly not the only one. Many of the newly introduced districts show a large number of predicted rides to the different parts of the city centre, which is not surprising, considering that it is the site of many services and entertainment options and people frequently have a need to travel there or return home after visiting there. What is interesting is the relative paucity of predicted east-west crosstown traffic; since the Helsinki public transport has traditionally been relatively weak in this direction, this could be expected to be supplemented by city bikes, although the longer distances involved could serve as a deterrent for this. This phenomenon would clearly bear further analysis of bike usage patterns especially in the northern parts of Helsinki.

## Further developments

While the system has already given quite promising and interesting results, many of its aspects can still be worked upon and refined. Both the predictive model, which is currently based on a technology called "random forest prediction", and the data used by it could be adjusted and made more accurate. In terms of data, one obvious refinement would be to use smaller regions like the Helsinki sub-districts, of which there are 148, allowing for even more accurate and fine-grained predictions and greater level of detail in analysing the current situation in existing districts. We already have the geographic data for the sub-districts, but unfortunately the demographic data on sub-district level was not conveniently available for the same period as the city bike data and would have to be provided by the City of Helsinki. In terms of methodology, the next step would be to examine the interaction of added districts by using the systm iteratively to include also rides from one new district to another new district. There is already an iterative version of the algorithm in place and it has been preliminarily tested, but the generation of the finished extra data required for the iterative tool did not fit within the scope of this project. By extending the scope of this project considerably, it would be possible to produce an interactive map tool that would allow adjusting the parameters of the predictions and displaying their details on many levels and from many viewpoints.
