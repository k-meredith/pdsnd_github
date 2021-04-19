import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['all','january','february','march','april','may','june','july','august','september','october','december']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Below while loops take user input, and check against valid entries. if in valid, will ask the user the enter another
    # value. converts user input to lower to ensure interoperability with rest of the code.
    # CITY Input
    while True:
        city = input("\nPlease select a city to view its data. Options include Chicago, New York City, and Washington\n").lower()
        # is city in dict city data?
        if city in CITY_DATA:
            # echos user entry if valid and continues
            print("You entered {}. Lets continue...".format(city.title()))
            break
        else:
            # informs user their entry is invalid and asks for new input
            print("\nYou did not enter a valid city. Please try again")
    # Month Input
    while True:
        month = input("\nPlease select a month to view its data, or state all to view everything\n").lower()
        if month in months:
            # echos user entry if valid and continues
            print("You entered {}. Lets continue...".format(month.title()))
            break
        else:
            # informs user their entry is invalid and asks for new input
            print("\nYou did not enter a valid option. Please try again")

    # establish valid entries for day input
    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
    # day input loop
    while True:
        day = input("\nPlease select a day to view its data, or state all to view everything\n").lower()
        if day in days:
            # echos user entry if valid and continues
            print("You entered {}. Lets continue...".format(day.title()))
            break
        else:
            # informs user their entry is invalid and asks for new input
            print("\nYou did not enter a valid option. Please try again")

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
   
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel, when applicable
    
    ARGS:
    df - Pandas DataFrame containing city data filtered by month and day
    
    Returns:
    no data is returne dupon completion of the function
    
    """
    
    # drop frist column of data; seems to be a transaction ID of sorts and this is
    # unneccessary data for what we are looking at. removing it will speed the program up
    df = df.drop(df.columns[0],axis = 1)

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month, if the user did not sort by month
    # gets series of number of renters per month
    df_months = df['month'].value_counts()
    # checks to see if data for mroe than one month is present.
    # if so, calcualtes the most popular via mode. if not, prints message
    # syaing there is no popular month since data is sorted by month
    if df_months.size > 1:
        popular_month = df['month'].mode()[0]
        print('The most popular month is',months[popular_month])
    else:
        print('The user sorted by month, so there is no most popular month')

    # Displays the most common day of week, if the user did not sort by date
    # gets series of number of renters per day
    df_dow = df['day_of_week'].value_counts()
    # checks to see if data for more than one day is present.
    # if so, calcualtes the most popular via mode. if not, prints message
    # syaing there is no popular day since data is sorted by day
    if df_dow.size > 1:
        popular_dow = df['day_of_week'].mode()[0]
        print('The Most Popular Day of the Week is',popular_dow)
    else:
        print('The user sorted by day, so there is no most popular day')
    
    # Displays the most common start hour
    # Create column that contains start hour
    df['hour'] = df['Start Time'].dt.hour
    # finds most popular start hour via mode
    popular_hour = df['hour'].mode()[0]
    print('The Most Popular Start Hour is',popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
     
    ARGS:
    df - Pandas DataFrame containing city data filtered by month and day
    
    Returns:
    no data is returned upon completion of the function
    
    """
    
    # drop frist column of data; seems to be a transaction ID of sorts and this is
    # unneccessary data for what we are looking at. removing it will speed the program up
    df = df.drop(df.columns[0],axis = 1)
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('The most Popular Start Station is:',popular_start)
    
    # TO DO: display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('The most Popular Start Station is:',popular_end)
    
    # TO DO: display most frequent combination of start station and end station trip
    df['start and end'] = df['Start Station']+' and '+df['End Station']
    popular_trip = df['start and end'].mode()[0]
    print('The most frequent combination of Start and End stations is',popular_trip)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
         
    ARGS:
    df - Pandas DataFrame containing city data filtered by month and day
    
    Returns:
    no data is returned upon completion of the function
    
    """
    
    # drop frist column of data; seems to be a transaction ID of sorts and this is
    # unneccessary data for what we are looking at. removing it will speed the program up
    df = df.drop(df.columns[0],axis = 1)
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # gather total trip durations in seconds
    total_duration = df['Trip Duration'].sum()
    # convert to seconds for time module
    total_time = time.gmtime(total_duration)
    # get formatted hour:minute:second breakdown
    formatted_total = time.strftime("%H:%M:%S",total_time)
    # print out total duration
    print('Users spent {} (Hours:Mins:Secs) using the bikeshare'.format(formatted_total))
    
    # TO DO: display mean travel time
    avg_duration = df['Trip Duration'].mean()
    # convert to seconds for time module
    avg_time = time.gmtime(avg_duration)
    # get formatted hour:minute:second breakdown
    formatted_avg = time.strftime("%H:%M:%S",avg_time)
    print('On Average, Users spent {} (Hours:Mins:Secs) on the rideshare'.format(formatted_avg))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """
    Displays statistics on bikeshare users, if data exists.
         
    ARGS:
    df - Pandas DataFrame containing city data filtered by month and day
    
    Returns:
    no data is returned upon completion of the function
    
    """
    
    # drop frist column of data; seems to be a transaction ID of sorts and this is
    # unneccessary data for what we are looking at. removing it will speed the program up
    df = df.drop(df.columns[0],axis = 1)
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    user_types = df['User Type'].value_counts()
    print('{} Subscribers and {} Customers rented bikes over this period.'.format(user_types ['Subscriber'], user_types['Customer']))
    
    # Displays counts of gender if the dataframe has a gender column
    if 'Gender' in df.columns:
        # pulls number of users who didnt list gender
        not_listed = df['Gender'].isnull().sum()
        # gets a series of the number of useres per gender
        genders = df['Gender'].value_counts()
        print('Of the renters during this time period, {} were male, {} were female, and {} did not list a gender.'.format(genders['Male'], genders['Female'], not_listed))
    else:
        print('The city you selected does not record gender data for its users')

    # Displays earliest, most recent, and most common year of birth
    # Checks to ensure that birth year data exists before proceeding
    if 'Birth Year' in df.columns:
        # First, records # of users wihtout a birth year listed and drops those rows
        not_listed = df['Birth Year'].isnull().sum()
        df = df.dropna(axis = 0)
        # With NaN vlaues removed, calculates min, max, and mode.
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print('The oldest renter was born in',oldest)
        print('The youngest renter was born in',youngest)
        print('The most common birth year in this group is',most_common)
        print('{} users did not report a birth year'.format(not_listed))
    else:
        print('The city you selected does not record birth year data for its users')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Displays 5 lines of raw data if user requests it         
    
    ARGS:
    df - Pandas DataFrame containing city data filtered by month and day
    
    Returns:
    no data is returned upon completion of the function
    
    """
    # sets follow up string to nothing, as only needed for a follow up inquiry
    follow_up = ""
    # sets row to display at index 0
    row = 0
    # Getting rid of columns we created to only output raw data
    df = df.drop(['month','day_of_week'], axis = 1)
    # Labels first column so it looks better
    df.columns.values[0] = 'ID'
    # loop requests user input, validates it, and processes the user's request
    # will ask user to vie wmore data if they answer yes.
    # will ask for another entry if user inputs an unanticiapted response
    while True:
        # User input request
        view_d = input('Would you like to view 5{} lines of raw data? (yes or no) \n'.format(follow_up)).lower()
        # if no, then breaks loop
        if view_d == 'no':
            break
        # if yes, then prints 5 rows of data
        if view_d == 'yes':
            print(df.iloc[row :(row+5)])
            # adds more to the user input request
            follow_up = " more"
            # increments the rows so next 5 are viewed
            row = row + 5
        # if invalid entry, will prompt user again.
        else:
            print('\nYour entry was not valid. Please try again\n.')
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
