## A better Helsinki with more city bikes
Helsinki city bikes have been widely used throughout Helsinki and have made transportation more convenient.
Many residents have had access to this convenient service, however there are some areas of Helsinki, which do not have city bikes yet. 
To be able to further expand the city bike network and provide the service to more people in a wider area, we trained a machine learning algorithm to predict how city bikes would be used in districts of Helsinki still without city bikes.
This way it will be possible to anticipate what expanding the network really means.

The districts without city bikes can be seen in grey below.
<div style="text-align: center;">
<iframe src="city_bike_network.html"
    sandbox="allow-same-origin allow-scripts"
    width="616"
    height="634"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>
</div>

## What properties make a district use city bikes?
Our trained machine learning algorithm considers the demographics of each district and correlates that to city bike usage statistics.
We believe that good indicators for city bike usage are demographics of districts such as total population, unemployment rate, age distribution, number of restaurants and shops and distribution of job types among many others. In total we use 212 different parameters for our model to get the best possible result.

<table style="text-align: center; font-size: 0.5em;">
  <thead></thead>
  <tr style="font-size: 0.5em;">
    <th>&nbsp;</th>
    <th colspan="2">Monday</th>
    <th colspan="2">Tuesday</th>
    <th colspan="2">Wednesday</th>
    <th colspan="2">Thursday</th>
    <th colspan="2">Friday</th>
    <th colspan="2">Saturday</th>
    <th colspan="2">Sunday</th>
    <th colspan="2">Total</th>
  </tr>  
  <tr>
      <th style="text-align: left;">District</th>
      <th>In</th>
      <th>Out</th>
      <th>In</th>
      <th>Out</th>
      <th>In</th>
      <th>Out</th>
      <th>In</th>
      <th>Out</th>
      <th>In</th>
      <th>Out</th>
      <th>In</th>
      <th>Out</th>
      <th>In</th>
      <th>Out</th>
      <th>In</th>
      <th>Out</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: left;">Kaarela (205)</td>
      <td>3922</td>
      <td>4111</td>
      <td>4059</td>
      <td>4188</td>
      <td>4126</td>
      <td>4249</td>
      <td>4069</td>
      <td>4016</td>
      <td>3329</td>
      <td>3468</td>
      <td>2801</td>
      <td>2979</td>
      <td>2754</td>
      <td>2728</td>
      <td>25064</td>
      <td>25741</td>
    </tr>
    <tr>
      <td style="text-align: left;">Tuomarinkylä (403)</td>
      <td>2600</td>
      <td>2679</td>
      <td>2744</td>
      <td>2559</td>
      <td>3058</td>
      <td>2753</td>
      <td>2616</td>
      <td>2483</td>
      <td>2479</td>
      <td>2032</td>
      <td>2145</td>
      <td>2116</td>
      <td>2013</td>
      <td>1848</td>
      <td>17658</td>
      <td>16472</td>
    </tr>
    <tr>
      <td style="text-align: left;">Itä-Pakila (405)</td>
      <td>3184</td>
      <td>3333</td>
      <td>3183</td>
      <td>3285</td>
      <td>3256</td>
      <td>3317</td>
      <td>2969</td>
      <td>3057</td>
      <td>2840</td>
      <td>2636</td>
      <td>2739</td>
      <td>2595</td>
      <td>2533</td>
      <td>2361</td>
      <td>20706</td>
      <td>20586</td>
    </tr>
    <tr>
      <td style="text-align: left;">Pukinmäki (502)</td>
      <td>3557</td>
      <td>3731</td>
      <td>3667</td>
      <td>3622</td>
      <td>3602</td>
      <td>3845</td>
      <td>3628</td>
      <td>3616</td>
      <td>3165</td>
      <td>3192</td>
      <td>2600</td>
      <td>2623</td>
      <td>2548</td>
      <td>2366</td>
      <td>22770</td>
      <td>22998</td>
    </tr>
    <tr>
      <td style="text-align: left;">Malmi (503)</td>
      <td>3023</td>
      <td>2707</td>
      <td>3052</td>
      <td>2647</td>
      <td>3369</td>
      <td>2764</td>
      <td>3248</td>
      <td>2776</td>
      <td>2197</td>
      <td>2546</td>
      <td>2047</td>
      <td>2042</td>
      <td>2016</td>
      <td>1944</td>
      <td>18954</td>
      <td>17429</td>
    </tr>
    <tr>
      <td style="text-align: left;">Suutarila (504)</td>
      <td>1423</td>
      <td>1409</td>
      <td>1482</td>
      <td>1403</td>
      <td>1437</td>
      <td>1559</td>
      <td>1480</td>
      <td>1404</td>
      <td>1154</td>
      <td>1185</td>
      <td>1068</td>
      <td>1133</td>
      <td>1105</td>
      <td>1031</td>
      <td>9151</td>
      <td>9127</td>
    </tr>
    <tr>
      <td style="text-align: left;">Puistola (505)</td>
      <td>1498</td>
      <td>1504</td>
      <td>1517</td>
      <td>1459</td>
      <td>1527</td>
      <td>1524</td>
      <td>1409</td>
      <td>1428</td>
      <td>1148</td>
      <td>1241</td>
      <td>1077</td>
      <td>1114</td>
      <td>1160</td>
      <td>1024</td>
      <td>9338</td>
      <td>9297</td>
    </tr>
    <tr>
      <td style="text-align: left;">Jakomäki (506)</td>
      <td>1738</td>
      <td>1715</td>
      <td>1810</td>
      <td>1682</td>
      <td>1772</td>
      <td>1803</td>
      <td>1783</td>
      <td>1626</td>
      <td>1416</td>
      <td>1437</td>
      <td>1236</td>
      <td>1247</td>
      <td>1235</td>
      <td>1133</td>
      <td>10992</td>
      <td>10645</td>
    </tr>
    <tr>
      <td style="text-align: left;">Mellunkylä (703)</td>
      <td>3870</td>
      <td>4817</td>
      <td>4976</td>
      <td>5697</td>
      <td>4872</td>
      <td>6266</td>
      <td>4479</td>
      <td>4988</td>
      <td>3788</td>
      <td>4153</td>
      <td>3210</td>
      <td>3304</td>
      <td>3330</td>
      <td>2953</td>
      <td>28528</td>
      <td>32181</td>
    </tr>
    <tr>
      <td style="text-align: left;">Vuosaari (704)</td>
      <td>2828</td>
      <td>3839</td>
      <td>3773</td>
      <td>4913</td>
      <td>4333</td>
      <td>5400</td>
      <td>3375</td>
      <td>4052</td>
      <td>3078</td>
      <td>3293</td>
      <td>2366</td>
      <td>2404</td>
      <td>2490</td>
      <td>2336</td>
      <td>22246</td>
      <td>26241</td>
    </tr>
    <tr>
      <td style="text-align: left;">Östersundom (801)</td>
      <td>2770</td>
      <td>2646</td>
      <td>2677</td>
      <td>2371</td>
      <td>3079</td>
      <td>2895</td>
      <td>2318</td>
      <td>2747</td>
      <td>2301</td>
      <td>2366</td>
      <td>2487</td>
      <td>2415</td>
      <td>2409</td>
      <td>2246</td>
      <td>18044</td>
      <td>17689</td>
    </tr>
  </tbody>
</table>

## Let's see what our model can do
We will look at one example district not in the city bike network yet, Vuosaari.

We can predict how many rides are taken from Vuosaari to each other district.
<div style="text-align: center;">
<iframe src="Vuosaari_outgoing.html"
    sandbox="allow-same-origin allow-scripts"
    width="616"
    height="634"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>
</div>
(For every day of the week and time of day...)

We can predict how many rides are taken to Vuosaari from each other district. 
<div style="text-align: center;">
<iframe src="Vuosaari_incoming.html"
    sandbox="allow-same-origin allow-scripts"
    width="616"
    height="634"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>
</div>

And use that for some statistics. Such as the net rides taken between Vuosaari and every other district.
<div style="text-align: center;">
<iframe src="Vuosaari.html"
    sandbox="allow-same-origin allow-scripts"
    width="616"
    height="634"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>
</div>
