
# Python Spreadsheet 2

Second attempt at a web-based python powered spreadsheet

## Structure

 * django site
   * handles web stuff
   * use sessions to coordinate with Service
 * Service
   * reads/writes sheet data on server
   * continuously running in backgroud
   * communicates with django site using pipes



