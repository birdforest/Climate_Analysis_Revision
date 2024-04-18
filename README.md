# Climate_Analysis
Challenge 10
## Analyze and Explore the Climat Data:
- Import the dependencies, Python SQL toolkit, and Object Relational Mapper
- Create engine to hawaii.sqlite, Reflect an existing database into a new mode using auto_map.base(), Save name to references name "station" and "measurement" and Create link from Python to DataBase
- Find the most recent date in the dataset by setting the date into scalar values with max indicating the most recent date
- Get the previous 12 months of data by subtracting the current date by 365 days (1 year ago)
- Perform a query to retrieve the data and precipitation scores, Sort the dataframe by date and use Pandas to plot the precipitation data. One important point is that the one_year_ago calculation, I applied timedelta(days=365). If i use days=365, the statistics displayed is going to be slightly different from the sample output. If i use days=366, then the statistics displayed is going to be the same as the sample output. I chose to stick with day=365 because it makes more sense to me.
## Exploratory Station Analysis
- Design a query to calculate the total number of stations in the dataset and a query to find the most active station by using the count function
- Calculate the lowest, highest and average temperature for the most active station with the filter function (set that to the most_active_station_id)
- Query the last 12 months of temperature observation data for the station and plot the results using a histogram
## Design the Climate App
- Import the dependencies, reflect on existing database into a new mode, reflect the tables, save references to each table and create the link from Python to the database
- Flask Setup / Routes by listing out all available API routes
- For the static API routes, create one for precipitation that returns the JSON representation of the dictionary that uses 'date' as the key and 'prcp' as the value, create one for stations that returns a JSON list of stations from the dataset, and create one for tobs that returns a JSON list of temperature observations for the previous year for the most active station
- For the dynamic API routes, create one for start_date and one for start_end_dates to return a JSON list of the minimum, average, and maximum temperature for a specific start and start-end range.
