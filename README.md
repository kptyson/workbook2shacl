# Transform Excel Workbook Metadata to SHACL for use in TopQuadrant's EDG Product

I got tired of fat-fingering the UI on [EDG](https://www.topquadrant.com/) when loading the [MITRE Att@ck](https://attack.mitre.org/resources/working-with-attack/) excel workbook, so I created this simple tool for adding the classes, property groups and properties to an EDG ontology

## Overview
This tool allows you to enrich an existing EDG SHACL ontology with metadata from an Excel workbook.
```
usage: workbook2shacl.py [-h] --input_ontology INPUT_ONTOLOGY
                         --output_ontology OUTPUT_ONTOLOGY --xlsx XLSX
                         [--exclude EXCLUDE] [--include INCLUDE]

Create SHACL elements in an EDG ontology from Excel workbook metadata

options:
  -h, --help            show this help message and exit
  --input_ontology INPUT_ONTOLOGY
                        A turtle format ontology file exported from EDG
  --output_ontology OUTPUT_ONTOLOGY
                        A turtle format ontology file containing SHACL
                        elements plus the input ontology
  --xlsx XLSX           Excel workbook file from which meta data is harvested
  --exclude EXCLUDE     Name worksheet to exclude
  --include INCLUDE     Name of worksheet to include

By default all worksheets are included

Process finished with exit code 0
```
## Structure of the generated ontology
One class is created that is a subclass of owl:Thing.  Its name is derived from the file name of the Excel workbook.

One class per worksheet is created.  Each is a subclass of the workbook class.

Each worksheet class gets a property group whose name is composed of the workbook file name and the worksheet name

Each column in the worksheet get a datatype property of type xsd:string.  No cardinality is specified, although that may change in latter releases.
## Usage
* Select your Excel workbook.  In my testing I used the [MITRE Att@ck](https://attack.mitre.org/resources/working-with-attack/) excel workbook
* Create an ontology in EDG and export it as a turtle file.  __DO NOT EXPORT IT AS A TRIG OR ZIP FILE__
* Specify:
  * The location of the ontology exported in the previous step
  * The location of your Excel workbook 
  * The location of the enriched ontology to be created.
  * The specific worksheets you wish to process.  The default it to process all of them.
  * The specific worksheets you wish excluded.  This is useful when you want to process most of the worksheets excluding a small number of worksheets.
* In EDG, import the newly enriched ontology.
* Edit the ontology specifying the public classes.
* You are now ready to import your workbook as a data graph
## Sample Execution
```
D:\PycharmProjects\workbook2shacl\venv\Scripts\python.exe D:\PycharmProjects\workbook2shacl\workbook2shacl.py 
    --xlsx D:\PycharmProjects\workbook2shacl\Input\enterprise-attack-v12.1.xlsx 
    --input_ontology D:\PycharmProjects\workbook2shacl\Input\mitre_att_ck.ttl 
    --output_ontology D:\PycharmProjects\workbook2shacl\Output\enriched_ontology.ttl 
    --exclude "Enterprise ATT&CK matrix" 
2022-12-31T13:48:52.186393 Checking command parameters
2022-12-31T13:48:54.375791 Reading D:\PycharmProjects\workbook2shacl\Input\mitre_att_ck.ttl
2022-12-31T13:48:54.539794 Reading D:\PycharmProjects\workbook2shacl\Input\enterprise-attack-v12.1.xlsx
2022-12-31T13:48:56.362793 Serializing to D:\PycharmProjects\workbook2shacl\Output\enriched_ontology.ttl
2022-12-31T13:48:56.436799 Done

Process finished with exit code 0
```