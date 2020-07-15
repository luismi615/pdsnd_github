import time
import pandas as pd
import numpy as np
import math

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    This function takes as input from the user raw filter and returns the filters in the rigth format

    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    vcity = False
    while vcity == False:
        city = input('Please, type the city you would like to explore (Chicago, New York City or Washington)').lower()
        if city in ['chicago','new york city','washington']:
            vcity = True
        else:
            print('That\'s not a valid city, try again!')

    # get user input for month (all, january, february, ... , june)
    month = None
    l_months = ('all','jan','feb','mar','apr','may','jun')
    while month not in l_months:
        month = input('Please type the month you would like to explore the data or all of them (All, Jan, Feb, Mar, Apr, May, Jun)').lower()
        if month not in l_months:
            print('That\'s not a valid month, try again!')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    l_days = ('all','mon','tue','wed','thr','fri','sat','sun')
    while day not in l_days:
        day = input('Please type the day you would like to explore the data or all of them (All, Mon, Tue, Wed, Thr, Fri, Sat, Sun )').lower()
        if day not in l_days:
            print('That\'s not a valid day, try again!')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    This function takes the previous fliters and load only the data that match with them. Returns this data.

    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['comb station'] = df['Start Station'] + ' - ' + df['End Station']
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        daysd = {'Mon':'Monday','Tue':'Tuesday','Wed':'Wednesday','Thr':'Thursday','Fri':'Friday','Sat':'Saturday','Sun':'Sunday'}
        df = df[df['day_of_week'] == daysd[day.title()]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    t_trips = df['Start Time'].count()
    print('Total Trips:\t',t_trips)
    p_month = df.groupby(['month'])['Trip Duration'].count().idxmax()
    trips_month = df[df['month'] == p_month]['month'].count()
    print('\nThe most frequent month: ', months[int(p_month) - 1])
    print('That\'s {}% of the trips'.format(trips_month/t_trips * 100))

    # display the most common day of week
    popular_day = df.groupby(['day_of_week'])['Trip Duration'].count().idxmax()
    trips_day = df[df['day_of_week'] == popular_day]['day_of_week'].count()
    print('\nThe most frequent day of week: ', popular_day)
    print('That\'s {}% of the trips'.format(trips_day / t_trips * 100))

    # display the most common start hour
    popular_hour = df.groupby(['hour'])['Trip Duration'].count().idxmax()
    trips_hour = df[df['hour'] == popular_hour]['hour'].count()
    print('\nMost Frequent Start Hour:\t', popular_hour)
    print('That\'s {}% of the trips'.format(trips_hour / t_trips * 100))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df.groupby(['Start Station'])['Trip Duration'].count().idxmax()
    numb_start_st = df[df['Start Station'] == popular_start_station]['Start Station'].count()
    print('The most frequent start station:\t', popular_start_station)
    print('Total of trips started:\t\t',numb_start_st)

    # display most commonly used end station
    popular_end_station = df.groupby(['End Station'])['Trip Duration'].count().idxmax()
    numb_end_st = df[df['End Station'] == popular_end_station]['End Station'].count()
    print('\nThe most frequent end station:\t', popular_end_station)
    print('Total of trips ended:\t\t', numb_end_st)

    # display most frequent combination of start station and end station trip
    popular_comb_station = df.groupby(['comb station'])['Trip Duration'].count().idxmax()
    numb_comb_st = df[df['comb station'] == popular_comb_station]['comb station'].count()
    print('\nThe most frequent Start-End stations: ', popular_comb_station)
    print('Total of trips:\t\t\t', numb_comb_st)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    print ('Total Trip Duration: {} sec'.format(travel_time))
    print ('That\'s almost {} days'.format(math.ceil(travel_time/86400)))

    # display mean travel time
    print ('\nMean travel time: {} sec'.format(df['Trip Duration'].mean()))
    print ('That\'s almost {} minutes'.format(math.ceil(df['Trip Duration'].mean()/3600)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    print('Types of Users\n', df.groupby(['User Type'])['User Type'].count())

    # Display counts of gender
    try:
        print('\nUsers by Genders\n', df.groupby(['Gender'])['Gender'].count())
    except:
        print('\nNo data available for gender in this city\n')

    # Display earliest, most recent, and most common year of birth
    try:
        print('\nEarliest year of birth from Users\t', int(df['Birth Year'].min()))
        print('\nMost Recent year of birth from Users\t', int(df['Birth Year'].max()))
        print('\nMost common year of birth from Users\t', int(df['Birth Year'].mode()[0]))
    except:
        print('\nNo data available for user\'s year of birth\n')

    #Display individual raw data
    print('\n Let\'s see some individual raw data\n')
    rdt = 'yes'
    count = 5
    while rdt == 'yes':
        for i in range(count - 5,count):
            try:
                print(df.iloc[i, 1 : len(df.columns) - 4])
                print('- ' * 40)
                count += 5
            except:
                print('I already displayed all the individual data, try another filter.')
                break
        rdt = input('Would you like to see more individual data? (Yes, No)').lower()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def main():
    '''This is the main function which calls all the previous funtions'''
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)


        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
