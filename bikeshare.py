import time
import datetime
import pandas as pd
import numpy as np
from IPython.display import display

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHES = {
     'january': 1,
     'february': 2,
     'march': 3,
     'april': 4,
     'may': 5,
     'june': 6
}

DAYS = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6
}

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    msg = 'Would you like to see data for Chicago, New York City, or Washington?'
    city_entered = False
    city = ''
    while city_entered != True:
        print(msg)
        city=input().lower()
        if city == 'chicago' or city == 'new york city' or city == 'washington':
            city_entered = True
        else:
            print('Invalid city, Please try again')

    msg = 'How do you want to filter the data?'
    print(msg)
    msg = 'Filter by month, enter 1\nFilter by day, enter 2\nNo filter, enter 3\n'
    filter_entered = False
    filter = 0
    while filter_entered != True:
        print(msg)
        filter = int(input().lower())
        if filter == 1 or filter == 2 or filter == 3:
            filter_entered = True
        else:
            print('Invalid filter, Please try again')

    # get user input for month (all, january, february, ... , june)
    msg ='Which month - January, February, March, April, May, or June?'
    month = 'all'
    while(filter == 1):
        print(msg)
        month = input().lower()
        if month == 'january' or month == 'february' or month == 'march' or month == 'april' or month == 'may' or month == 'june' or month == 'all':
            break
        else:
            print('Invalid month, Please try again')


    # get user input for day of week (all, monday, tuesday, ... sunday)
    msg ='Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?'
    day = 'all'
    while(filter == 2):
        print(msg)
        day = input().lower()
        if day == 'monday' or day == 'tuesday' or day == 'wednesday' or day == 'thursday' or day == 'friday' or day == 'saturday' or day == 'sunday' or day == 'all':
            break
        else:
            print('Invalid day, Please try again')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA.get(city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    df['Start End Stations'] = df['Start Station'].apply(str) +', '+ df['End Station'].apply(str)
    df['Travel Time'] = (df['End Time'] - df['Start Time'])
    df['Travel Time'] = df['Travel Time'] / np.timedelta64(1, 's')

    if month != 'all':
        df = df.loc[(df['month'] == MONTHES[month])]

    if day != 'all':
        df = df.loc[(df['day'] == DAYS[day])]


    counter = 1
    msg = 'Would You like to see raw data?'
    while True:
        print(msg)
        ans = input().lower()
        if ans == 'yes' or ans == 'no':
            if ans == 'no':
                break
            else:
                display(df.iloc[counter:counter + 5])
                counter += 5
        else:
            print('Invalid answer, Please try again')

    return df


def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mcm = df['month'].value_counts()[:1].index.tolist()[0] #mcm: most common month
    for month in MONTHES.keys():
        if MONTHES[month] == mcm:
            mcm = month
    print('Most common month:', ' ', mcm, ' with frequency of: ', df['month'].value_counts()[:1].tolist()[0])

    # display the most common day of week
    mcd = df['day'].value_counts()[:1].index.tolist()[0] #mcd: most common day
    for day in DAYS.keys():
        if DAYS[day] == mcd:
            mcd = day
    print('Most common day:', ' ', mcd, ' with frequency of: ', df['day'].value_counts()[:1].tolist()[0])

    # display the most common start hour
    mch = df['hour'].value_counts()[:1].index.tolist()[0] #mch: most common hour
    print('Most common hour:', ' ', mch, ' with frequency of: ', df['hour'].value_counts()[:1].tolist()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mcss = df['Start Station'].value_counts()[:1].index.tolist()[0] #mcss: most common start station
    print('Most commonly used start station:', ' ', mcss, ' with frequency of: ', df['Start Station'].value_counts()[:1].tolist()[0])

    # display most commonly used end station
    mces = df['End Station'].value_counts()[:1].index.tolist()[0] #mces: most common end station
    print('Most commonly used end station:', ' ', mces, ' with frequency of: ', df['End Station'].value_counts()[:1].tolist()[0])

    # display most frequent combination of start station and end station trip
    mcses = df['Start End Stations'].value_counts()[:1].index.tolist()[0] #mcses: most common start end stations
    print('Most commonly used start and end stations together:', ' ', mcses, ' with frequency of: ', df['Start End Stations'].value_counts()[:1].tolist()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    ttt = df['Travel Time'].sum() # ttt: total travel time
    days = int(ttt / (3600 * 24))
    ttt = ttt % (3600 * 24)
    hours = int(ttt / 3600)
    ttt = ttt % 3600
    minutes = int(ttt / 60)
    ttt = ttt % 60
    print('total travel time: ', days, 'd:', hours, 'h:', minutes, 'm:', int(ttt), 's')

    # display mean travel time
    mtt = df['Travel Time'].mean() # ttt: total travel time
    days = int(mtt / (3600 * 24))
    mtt = mtt % (3600 * 24)
    hours = int(mtt / 3600)
    mtt = mtt % 3600
    minutes = int(mtt / 60)
    mtt = mtt % 60
    print('mean travel time: ', days, 'd:', hours, 'h:', minutes, 'm:', int(mtt), 's')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    cut = df['User Type'].nunique() #cut :counts of user types
    print('Counts of user types: ',cut)

    # Display counts of gender
    if city =='chicago' or city =='new york city':
        cog = df['Gender'].nunique() #cog :counts of genders
        print('Counts of genders: ',cog)
    else:
        print('This city has no column "gender"')

    # Display earliest, most recent, and most common year of birth
    if city == 'chicago' or city == 'new york city':
        df = df.dropna(axis=0, subset=['Birth Year'])
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        mcy = df['Birth Year'].value_counts().index.tolist()[0] #mcy: most recent year
        print('Earliest year: ',earliest,',Most recent: ',recent,',Most common year: ',mcy)
    else:
        print('This city has no column "Birth Year"')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
