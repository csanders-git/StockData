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

## Breach Type
The VCDB data comes pre-labeled with types. These types were considered too specific for our use cases. Existing VCDB data that was not in scope maintains its existing labeling. In scope data was updated to the standard used by Privacy Right Clearinghouse. That standard is as follows:

* Unintended disclosure (DISC) - Sensitive information posted publicly on a website, mishandled or sent to the wrong party via email, fax or mail.
* Hacking or malware (HACK) - Electronic entry by an outside party, malware and spyware.
* Payment Card Fraud (CARD) - Fraud involving debit and credit cards that is not accomplished via hacking. For example, skimming devices at point-of-service terminals.
* Insider (INSD) - Someone with legitimate access intentionally breaches information - such as an employee or contractor.
* Physical loss (PHYS) - Lost, discarded or stolen non-electronic records, such as paper documents
* Portable device (PORT) - Lost, discarded or stolen laptop, PDA, smartphone, portable memory device, CD, hard drive, data tape, etc
* Stationary device (STAT) - Lost, discarded or stolen stationary electronic device such as a computer or server not designed for mobility.
* Unknown or other (UNKN)

## Stock information
In this version of the release stock information comes from Financial Modeling Prep (https://financialmodelingprep.com/). Financial Modeling Prep provides a free API. Information on our usage of the API can be found in `tools/fetch_stock_info`. This script will read from our dataset sheet and downloaded all NYSE and NASDAQ stocks with the symbols listed. The data will be available in the created `data` subfolder and will be broken down by stock symbol on a day by day cadence from 1998-2020 (if available).

Some of the information provided by this service is incomplete. The following companies were updated from data on cnvesting.com (https://www.investing.com). These were transformed to match the format of the data downloaded from Financial Modeling Prep.
VWAP values are just placeholders as the needed on these stocks are just placeholders as the needed information to perform the calculation wasn't present.

* Express script's stock info was downloaded from https://www.investing.com/equities/express-scripts-inc-historical-data
* DirectTV's stock info was downloaded from https://www.investing.com/equities/directv-historical-data:
* Barnes and Nobel's stock info was downloaded from https://www.investing.com/equities/barnes---noble-inc-historical-data
* Aetna's stock info was downloaded from https://www.investing.com/equities/aetna-inc-historical-data
* Time warner's stock info was downloaded from https://www.investing.com/equities/time-warner-historical-data
