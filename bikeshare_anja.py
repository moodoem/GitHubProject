import time
import pandas as pd
import numpy as np
# import a calendar for complete names for moth and weekday
import calendar as calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Here we will explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Which city do you want to analyze? Please choose from the following: Chicago, New York City, Washington.\n")
        
        # use lower case to make entries case-insensitive
        city = city.lower()
        
        # avoid input error for city
        if city not in ('new york city', 'chicago', 'washington'):
            print("This is not a valid city. Please enter a valid city.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month do you want to analyze? Please choose from the following: January, February, March, April, May, June, all.\n")
        
        # use lower case to make entries case-insensitive
        month = month.lower()
        
        # avoid input error for month
        if month not in ('january', 'february', 'march', 'april', 'may', 
                         'june', 'all'):
            print("This is not a valid month. Please enter a valid month.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day do you want to analyze? Please choose from the following: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, all.\n")
        
        # user lower case to make entries case-insensitive
        day = day.lower()
        
        # avoid input error for day of week
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                       'saturday', 'sunday', 'all'):
            print("This is not a valid day. Please enter a valid day.")
            continue
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load CSV file for selected city
    df = pd.read_csv(CITY_DATA[city])
    
    # convert 'Start Time' column from plain text strings into proper Pandas datetime object
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month
    df['Month'] = df['Start Time'].dt.month
    
    # extract day
    df['Weekday'] = df['Start Time'].dt.weekday
    
    # filter data for selected month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]
    
    # filter data for selected day
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day) 
        df = df[df['Weekday'] == day]
    
    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month    
    # MONTH 1: list of names for months from calendar
    list(calendar.month_name)
    
    # MONTH 2: determine most common month
    common_month = df['Month'].value_counts().idxmax()
    
    # MONTH 3: print result for most common month
    if month != 'all':
        print('Since you selected',month.title(),', the most common month is', calendar.month_name[common_month], '.\n')
    
    else:
        print('The most common month is', calendar.month_name[common_month], '.\n')
    

    # display the most common day of week    
    # DAY 1: list of names for days from calendar    
    list(calendar.day_name)
    
    # DAY 2: determine most common day
    common_day = df['Weekday'].value_counts().idxmax()
    
    # DAY 3: print result for most common day
    if day != 'all':
        print('Since you selected',day.title(),', the most common day is', calendar.day_name[common_day], '.\n')    
    else:
        print('The most common weekday is', calendar.day_name[common_day], '.\n')
    
        
    # display the most common start hour
    # HOUR 1: new variable for hour extracted from 'Start Time'
    df['Start Hour'] = df['Start Time'].dt.hour    
    
    # HOUR 2: print result for most common start hour
    print('The most common start hour is', df['Start Hour'].value_counts().idxmax(), 'o\'clock.\n')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is', df['Start Station'].value_counts().idxmax(), '.\n')

    # display most commonly used end station
    print('The most commonly used end station is', df['End Station'].value_counts().idxmax(), '.\n')

    # display most frequent combination of start station and end station trip
    # STATION COMBINATION 1: Create new column 'Station Combination' with combined start and end station
    df['Station Combination'] = df['Start Station'] + ' (from) and ' + df['End Station'] + ' (to)'
    
    # STATION COMBINATION 2: print result for most common station combination
    print('The most common station combination is', df['Station Combination'].value_counts().idxmax(), '.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # TOTAL TIME 1: calculate total travel time in seconds
    totaltriptime_sec = df['Trip Duration'].sum()
    
    # TOTAL TIME 2: calculate hours from seconds; round to two decimals
    totaltriptime_h = round(totaltriptime_sec / 60 / 60 ,2)
    
    # TOTAL TIME 3: print result for total travel time
    print('The total travel time is', totaltriptime_h, 'hours.\n')

    # display mean travel time
    # MEAN TIME 1: calculate mean travel time in seconds
    meantriptime_sec = df['Trip Duration'].mean()
    
    # MEAN TIME 2: calculate minutes from seconds; round to two decimals
    meantriptime_min = round(meantriptime_sec / 60  ,2)    
    
    # MEAN TIME 3: display result for mean travel time
    print('The mean travel time is', meantriptime_min, 'minutes.\n')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # USER TYPE 1: get the 'User Type' column as a NumPy array
    usertypes = df['User Type'].values
    
    # USER TYPE 2: count occurences of each user type
    count_subscriber  = (usertypes == 'Subscriber').sum()
    count_customer = (usertypes == 'Customer').sum()
    
    # USER TYPE 3: print results for user type counts
    print('The number of subscribers in is:',count_subscriber,'\n')
    print('The number of customers in is:',count_customer,'\n')

    # Display counts of gender
    # Display earliest, most recent, and most common year of birth
    # distinguish between Washington and the other two cities, since no gender and birth date data is available for Washington
    if city.title() != 'Washington':
        # counts of gender
        # GENDER 1: get the 'Gender' column as a NumPy array
        gender = df['Gender'].values
        
        # GENDER 2: count the occurences of each gender
        count_male  = (gender == 'Male').sum()
        count_female = (gender == 'Female').sum()
        
        # GENDER 3: print result for gender counts
        print('The number of male users in is:',count_male,'\n')
        print('The number of female users in is:',count_female,'\n')
    
        # BIRTHYEAR 1: get the 'Birth Year' column as a NumPy array
        birthyear = df['Birth Year'].values
        
        # BIRTHYEAR 2: extract unique non-NaN birth years
        unique_birthyear = np.unique(birthyear[~np.isnan(birthyear)])
        
        # BIRTHYEAR 3: get latest birth year
        latest_birthyear = unique_birthyear.max()
        
        # BIRTHYEAR 4: get earliest birth year
        earliest_birthyear = unique_birthyear.min()
        
        # BIRTHYEAR 5: print results for latest, earliest and most common birth year
        print('The user\'s most recent birth year of users is:', latest_birthyear,'\n')
        print('The earliest user\'s birth year is:', earliest_birthyear,'\n')   
        print('The most common user\'s birth year is:', df['Birth Year'].value_counts().idxmax(),'\n')
    
    else:
        # print result for Washington
        print('Unfortunately, no gender and birth year data is available for Washington.\n')

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# raw data is displayed upon request by the user
# function to display raw data  
def raw_data(df):
    # index i to keep track of current line
    i = 1
    while True:
        showrawdata = input('\nWould you like to see 5 lines of raw data? Please type yes or no.\n')
        if showrawdata.lower() == 'yes':
            # print 5 lines of raw data
            print(df[i:i+5])
            
            # index
            i = i+5
            
        else:
            # break loop if user does not want to see raw data
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # add arguments city, month, day to time_stats function
        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        # add argument city to user_stats function
        user_stats(df, city)
        
        # display raw data
        raw_data(df)
        
  
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

###############################################################################
######              Resources used 
#
# Udacity Introduction to Python programming course videos and notes
#
# Udacity project description and Rubric
#
# https://www.askpython.com/python/examples/python-user-input#:~:text=Python%20User%20Input%20from%20Keyboard%20%E2%80%93%20input%20%28%29,for%20the%20user%20input.%20...%20More%20items...%20
# 
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
# 
# https://stackoverflow.com/questions/51603690/extract-day-and-month-from-a-datetime-object
#
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.month.html
#
# https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.weekday.html
#
# https://www.codespeedy.com/filter-rows-of-dataframe-in-python/?msclkid=bd629acbb45a11ecab45cfffe288aac0
#
# https://datascientyst.com/get-most-frequent-values-pandas-dataframe/#:~:text=To%20get%20the%20most%20frequent,value%20that%20appears%20most%20often.
#
# https://www.tutorialspoint.com/python/string_title.htm#:~:text=Python%20String%20title%20%28%29%20Method%201%20Description.%20Python,shows%20the%20usage%20of%20title%20%28%29%20method.%20?msclkid=2146553bb44d11ec8016e0c8f789849f
#
# https://stackoverflow.com/questions/36341484/get-day-name-from-weekday-int
#
# https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.hour.html
#
# https://stackoverflow.com/questions/19377969/combine-two-columns-of-text-in-pandas-dataframe
#
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.values.html
#
# https://stackoverflow.com/questions/28663856/how-to-count-the-occurrence-of-certain-item-in-an-ndarray
#
# https://stackoverflow.com/questions/28940412/how-to-find-the-unique-non-nan-values-in-a-numpy-array?msclkid=2a22e900b45411ec87fa194c60c6cefd
