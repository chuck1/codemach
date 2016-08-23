
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

## Testing

To test, open two terminals. In one, run "./service/start.py". In the other, navigate to pyspread\_site and run "python manage.py runserver 0.0.0.0 9001".

