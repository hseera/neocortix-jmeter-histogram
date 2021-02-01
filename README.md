![index](https://github.com/hseera/neocortix-jmeter-histogram/blob/main/image/histogram.png)

# Neocortix Jmeter Histogram
This simple utility generates a Jmeter histogram for a given transaction name for the batch test executed on the Neocortix infrastructure. 

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

## Authors

* **Harinder Seera** - *Initial work* - [OzPerf](https://ozperf.com/)

If you would like to contribute to this project, please reachout to me.

## License

This project is licensed under the Apache License - see the [LICENSE.md](LICENSE.md) file for details

