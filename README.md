![index](https://github.com/hseera/neocortix-jmeter-histogram/blob/main/images/histogram.png)

# Neocortix Jmeter Histogram
![Language Python](https://img.shields.io/badge/%20Language-python-blue.svg) [![MIT License](http://img.shields.io/badge/License-MIT-blue.png)](LICENSE)

[![GitHub Last Commits](https://img.shields.io/github/last-commit/hseera/neocortix-jmeter-histogram.svg)](https://github.com/hseera/neocortix-jmeter-histograms/commits/) [![GitHub Size](https://img.shields.io/github/repo-size/hseera/neocortix-jmeter-histogram.svg)](https://github.com/hseera/neocortix-jmeter-histogram/)
[![Open GitHub Issue](https://img.shields.io/badge/Open-Incident-brightgreen.svg)](https://github.com/hseera/neocortix-jmeter-histogram/issues/new/choose)
[![GitHub Open Issues](https://img.shields.io/github/issues/hseera/python-utilities?color=purple)](https://github.com/hseera/neocortix-jmeter-histogram/issues?q=is%3Aopen+is%3Aissue)
[![GitHub Closed Issues](https://img.shields.io/github/issues-closed/hseera/python-utilities?color=purple)](https://github.com/hseera/neocortix-jmeter-histogram/issues?q=is%3Aclosed+is%3Aissue)

This simple utility generates a Jmeter histogram for a given transaction name for the batch test executed on the Neocortix infrastructure.

A secondary script (neocortix_jmeter_multi_graphs.py) allows you to generate multiple graphs as shown below. 
Note: This script is Work In Progress.

![index](https://github.com/hseera/neocortix-jmeter-histogram/blob/main/images/graphs.png)

---
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
Note: 
1: The script was test on Windows OS.
2: There are sample data files (TestPlan_*.csv) which you can use to test & also understand how the script works.


### Prerequisites

What things you need to execute the script

```
1: python 3.5
2: numpy, panda & matlab packages

```

### Execution

```
1: Make sure above prerequisite are met first.
2: Copy all the TestPlan_result_*.csv files generated from the Neocotrix test run and place them in the same folder as the script.
3: Replace the default value for TRANSACTION_NAME with the transaction name for which you want to generate histrogram.
4: Run the python script
```

### Enhancements
```
1: Pass transaction name as parameter to the script.
2: Make sure the mean text value doesn't overflow the chart.
```

## Contribute

If you would like to contribute to this project, please reachout to me. Issues and pull requests are welcomed too.

## Author
[<img id="github" src="./images/github.png" width="50" a="https://github.com/hseera/">](https://github.com/hseera/)    [<img src="./images/linkedin.png" style="max-width:100%;" >](https://www.linkedin.com/in/hpseera) [<img id="twitter" src="./images/twitter.png" width="50" a="twitter.com/HarinderSeera/">](https://twitter.com/@HarinderSeera) <a href="https://twitter.com/intent/follow?screen_name=harinderseera"> <img src="https://img.shields.io/twitter/follow/harinderseera.svg?label=Follow%20@harinderseera" alt="Follow @harinderseera" /> </a>          [![GitHub followers](https://img.shields.io/github/followers/hseera.svg?style=social&label=Follow&maxAge=2592000)](https://github.com/hseera?tab=followers)


## License

This project is licensed under the Apache License - see the [LICENSE.md](LICENSE.md) file for details

