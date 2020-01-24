# Shmoocon 2020 update

## Verifying the data

The original, unenriched, data is available from its respective sources. Unfiltered data is available in `dataset.csv` for further research.

To generate the data used in the presentation you should run the jupyter notebook. This can be accomplished via the following:

```
pip install -r requirements.txt
jupyter notebook
```

# Breach data
The breach data comes from three different sources:

* VERIS Community Database (VCDB) (https://github.com/vz-risk/VCDB)
* Privacy Rights Clearinghouse (https://privacyrights.org/data-breaches)
* Wikipedia (https://en.wikipedia.org/wiki/List_of_data_breaches)

The original work on this effort was guided by Wikipedia. It became clear that this was not an exhaustive list, even of widely known breaches. As a result for more recent iterations more work was put into leveraging additional sources. These sources were combined, enriched, and corrected where needed to produce `dataset.csv`. For our research we identified breaches of publicly traded companies (NASDAQ or NYSE although the data is enriched with other exchanges as well) and determined if the breach affected over 100 customer records. Only records matching this description were included in the final 153 samples. We have isolated these samples as `dataset-samples.csv`.

## Stock information
In this version of the release stock information comes from Financial Modeling Prep (https://financialmodelingprep.com/). Financial Modeling Prep provides a free API. Information on our usage of the API can be found in `tools/fetch_stock_info`. This script will read from our dataset sheet and downloaded all NYSE and NASDAQ stocks with the symbols listed. The data will be available in the created `data` subfolder and will be broken down by stock symbol on a day by day cadence from 1998-2020 (if available).

Some of the information provided by this service is incomplete. The following companies were updated from data on cnvesting.com (https://www.investing.com). These were transformed to match the format of the data downloaded from Financial Modeling Prep.
VWAP values are just placeholders as the needed on these stocks are just placeholders as the needed information to perform the calculation wasn't present.

* Express script's stock info was downloaded from https://www.investing.com/equities/express-scripts-inc-historical-data
* DirectTV's stock info was downloaded from https://www.investing.com/equities/directv-historical-data:
* Barnes and Nobel's stock info was downloaded from https://www.investing.com/equities/barnes---noble-inc-historical-data
* Aetna's stock info was downloaded from https://www.investing.com/equities/aetna-inc-historical-data
* Time warner's stock info was downloaded from https://www.investing.com/equities/time-warner-historical-data
