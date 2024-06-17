# Repository for exploring and building a forecasting model/application in order to predict the discharge on the Gallatin River.

I did a project trying to forecast the river flow for the Gallatin river for my Time Series Analysis class. I didn't find a valid model and am interested in finding a better solution so I can create an app for myself to predict the water levels on the gallatin river. This is will be the groundwork for that app, including the model(s), data pipeline to get live data from the area, and a simple frontend to display the results.

## Data sources

Snotel data (Shower Falls Location 754):
- Sites for Montana
https://nwcc-apps.sc.egov.usda.gov/site-plots/#MT
- Rest API
https://wcc.sc.egov.usda.gov/awdbRestApi/swagger-ui/index.html
- User guide pdf (with variable code names) 
https://www.nrcs.usda.gov/sites/default/files/2023-03/AWDB%20Web%20Service%20User%20Guide.pdf

Water data (station number 06043500):
- USGS Site
https://nwis.waterdata.usgs.gov/nwis
- USGS Dashboard for Gallatin Gateway
https://dashboard.waterdata.usgs.gov/api/gwis/2.1.1/service/site?agencyCode=USGS&siteNumber=06043500&open=82374
- USGS Dashboard for Big Sky (site 06043120)
https://dashboard.waterdata.usgs.gov/api/gwis/2.1.1/service/site?agencyCode=USGS&siteNumber=06043120&open=247869
- USGS Water Services
https://waterservices.usgs.gov/
