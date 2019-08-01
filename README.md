# AVID Media composer scripts
## Effects Marker List
### Description
Takes an effects summary report from AVID Media Composer and searches for a given effect. It will then create a new tab delimited text file.  That file is formatted so that it can be brought into AVID Media Composer as a marker list.  'Marker Name', 'Start timecode', 'Track Number', 'Marker Color', 'Comment'.

### Prerequisites
- Install and active Python 3
- Pandas  
      ```pip install pandas```
- Copy and paste effects summary into a next blank text file.  

### Bugs
- Text file encoding out of Media Composer throws an 'utf-8' decoding error.  Current work around is copying media into a new blank text file, saving and then using that text file to run in the python script.
