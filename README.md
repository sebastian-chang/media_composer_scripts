# AVID Media composer scripts
## Effects Marker List
### Description
Takes an effects summary report from AVID Media Composer and searches for a given effect. It will then create a new tab delimited text file.  That file is formatted so that it can be brought into AVID Media Composer as a marker list.  'Marker Name', 'Start timecode', 'Track Number', 'Marker Color', 'Comment'.

### Prerequisites
- Python 3
- Pandas  
      ```pip install pandas```
- Copy and paste effects summary into a next blank text file.
- Remove all contents before  
      ```----- Effect Plug-in Summary: -----```

