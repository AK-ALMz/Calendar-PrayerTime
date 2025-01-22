import json
import urllib.request
from datetime import datetime, timedelta
#Temporary Variables, remove later when making a function
def find_prayer_times(city,country,date_list):
    #Temporary variables for testing

    #initialize an empty list for each prayer time. Index 0 would represent the start date, so on and so forth.
    fajr_times = []
    dhuhr_times = []
    asr_times = []
    maghrib_times = []
    isha_times = []

    for date in date_list:
        date = date.strftime('%d-%m-%Y')
        #Read HTTPResponse from the url
        response = urllib.request.urlopen(f"https://api.aladhan.com/v1/timingsByCity/{date}?city={city}&country={country}")

        #decode the HTTPResponse into JSON
        dataJSON = response.read().decode('utf-8')

        #Decode JSON into python dictionary
        data = json.loads(dataJSON)

        #append the prayer time to its corresponding list. values are in the format "HR:MIN".
        fajr_times.append(data['data']['timings']['Fajr'])
        dhuhr_times.append(data['data']['timings']['Dhuhr'])
        asr_times.append(data['data']['timings']['Asr'])
        maghrib_times.append(data['data']['timings']['Maghrib'])
        isha_times.append(data['data']['timings']['Isha']) 
        
    #Obtaining the timezone to be set in the calendar.
    timezone = data['data']['meta']['timezone']
    #generate lists that contain each prayer time
    return timezone,fajr_times,dhuhr_times,asr_times,maghrib_times,isha_times

def get_date_range(start_date_str, end_date_str):
    """
    Generate a list of dates between start and end dates (inclusive).
    
    Parameters:
    start_date_str (str): Start date in DD-MM-YYYY format
    end_date_str (str): End date in DD-MM-YYYY format
    
    Returns:
    list: List of datetime objects representing each date in the range
    """
    try:
        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date_str, '%d-%m-%Y')
        end_date = datetime.strptime(end_date_str, '%d-%m-%Y')
        
        # Validate date range
        if start_date > end_date:
            raise ValueError("Start date must be before or equal to end date")
        
        # Generate list of dates
        date_range = []
        current_date = start_date
        
        while current_date <= end_date:
            date_range.append(current_date)
            current_date += timedelta(days=1)
            
        return date_range
    
    except ValueError as e:
        if "time data" in str(e):
            return "Error: Invalid date format. Please use DD-MM-YYYY format."
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: An unexpected error occurred - {str(e)}"

#start = input("Enter start date DD-MM-YYYY:")
#end = input ("Enter End date:")
#dates = get_date_range(start,end)
#print(dates)
