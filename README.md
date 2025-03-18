# DataCollector

## how to run:
- clone the repository
```
git clone https://github.com/atik8055BUET/DataCollector
```
- open the folder in vscode
- run the `DataCollector.py`

## Inputs of the program
### starting index
Everytime, When you start the program, It will take the starting index from where, We will collect data from bd-pratidin.
- if you run this program for the 1st time, take your starting index from table
- if you have already run this program, there may be created a `trainData.csv`. Look at the last line of this file which will look like this.
```
<#END-ASTHA#>,https://www.bd-pratidin.com/national/2025/03/18/{starting index},2025-03-19
```
**for example:**
```
<#END-ASTHA#>,https://www.bd-pratidin.com/national/2025/03/18/1263,2025-03-19
```
Then,
- your starting index will be: 1263

### Ending index
Enter your ending index from the table. It is optional, you can make it blank.

| Name | starting index | ending index |
| --- | --- | --- |
|atik |1 | 220000|
|tahmid | 220000 | 440000 |
|tanvir| 440000| 660000|
|lamia|660000|880000|
|rahim|880000|1100000|

**Here you go... Enjoy Collecting data...**
