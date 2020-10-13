## A better Helsinki with more city bikes
Helsinki city bikes have been widely used throughout Helsinki and have made transportation more convenient.
Many residents have had access to this convenient service, however there are some areas of Helsinki, which do not have city bikes yet. 
To be able to further expand the city bike network and provide the service to more people in a wider area, we trained a machine learning algorithm to predict how city bikes would be used in districts of Helsinki still without city bikes.
This way it will be possible to anticipate what expanding the network really means.

The districts without city bikes can be seen in grey below.
<iframe src="city_bike_network.html"
    sandbox="allow-same-origin allow-scripts"
    width="100%"
    height="650"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>

## What properties make a district use city bikes?
Our trained machine learning algorithm considers the demographics of each district and correlates that to city bike usage statistics.
We believe that good indicators for city bike usage are demographics of districts such as total population, unemployment rate, age distribution, number of restaurants and shops and distribution of job types among many others. In total we use 212 different parameters for our model to get the best possible result.

## Let's see what our model can do
We will look at one example district not in the city bike network yet, Vuosaari.

We can predict how many rides are taken from Vuosaari to each other district. 
<iframe src="Vuosaari_outgoing.html"
    sandbox="allow-same-origin allow-scripts"
    width="100%"
    height="650"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>
(For every day of the week and time of day...)

We can predict how many rides are taken to Vuosaari to each other district. 
<iframe src="Vuosaari_incoming.html"
    sandbox="allow-same-origin allow-scripts"
    width="100%"
    height="650"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>

And use that for some statistics. Such as the net rides taken between Vuosaari and every other district.
<iframe src="Vuosaari.html"
    sandbox="allow-same-origin allow-scripts"
    width="100%"
    height="650"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>
