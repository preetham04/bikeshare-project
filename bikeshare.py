import numpy as np
import pandas as pd
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['all','january','february','march','april','may','june']
days = ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    print("Hello Let\'s explore some US bikeshare data!")
    while True:
        city = input("\nEnter the name of the city you wish to explore!\n Chicago,New York City,Washington\n").lower()
        if city not in CITY_DATA:
            print("\nYou have entered the wrong city!\n")
            continue
        else:
            print("\nYou have selected " + city + ". Lets continue with the next selection\n")
            while True:
                month_name = input("\nEnter the month you wish to explore.\n(Type all or january,february,march,april,may,june)\n").lower()
                if month_name not in months:
                    print("\nYou entered the wrong month!\n")
                    continue
                else:
                    print("\nYou have selected " + month_name + ". Lets continue with the next selection\n")
                    while True:
                        day = input("\nEnter the day of the week you wish to explore.\n(Type all or sunday,monday,tuesday,wednesday,thursday,friday,saturday)\n").lower()
                        if day not in days:
                            print("\nYou have entered the wrong day!\n")
                        else:
                            print("\nYou have selected " + day +".")
                            print('-'*40)
                        return city,month_name,day


#print(get_filters())
def load_data(city,month,day):
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding
        month_data = ['january','february','march','april','may','june']
        month = month_data.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        #filter by day of week if applicable
        if day != 'all':
            #filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    print("\n Calculating the most frequent times of travel...\n")
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    #print("\ncommon month\n" + str(common_month).title())
    print("\nThe most common month from the filtered data would be :  \n" + months[common_month].title())

    #TO DO: display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print("\nThe most common day of week from the filtered data would be:  \n " + common_day_of_week)

    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    print("\nThe most common start hour from the filtered data would be:   \n " + str(common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("\nThe most commonly used start station from the filtered data is:\n " + common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("\nThe most commonly used end station from the filtered data is:\n" + common_end_station)

    # TO DO: display most common trip from start to end (i.e., most frequent combination of start station and end station)
    df['Start to End'] = df['Start Station'].str.cat(df['End Station'],sep = ' To ')
    combo = df['Start to End'].mode()[0]
    print("\nThe most frequent combination of start and end stations from the filtered data are :\n" + combo)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_starts(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("\nTotal travel time for the filtered data is:\n" +str(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("\nMean travel time for the filtered data is:\n" + str(mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nThe user type count from the filtered data is:\n" + str(user_types))

    # TO DO: Display counts of gender
    #gender_count = df['Gender'].value_counts()
    #print("\n Gender count\n" + str(gender_count))
    try:
        gender_count = df['Gender'].value_counts()
        print("\nGender count\n" + str(gender_count))
    except KeyError:
        print("\nGender data is missing in certain columns of the filtered data\n")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]
        print("\nEarliest birth year from the filtered data:    " + str(earliest_birth))
        print("\nRecent birth year from the filtered data:     " + str(recent_birth))
        print("\nCommon birth year from the filtered data:     " + str(common_birth))
    except KeyError:
        print("\nBirth Year data is missing in certain columns of the filtered data")
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def display_data(df):

    """
    Displays raw data on user request
    """
    next = 0
    print(df.head())
    while True:
        next_data = input("\nWould you like to view the next 5 rows of data. Enter 'yes' to view data or 'no' to exit\n").lower()
        next += 5
        if next_data == "yes":
            print(df.iloc[next:next+5])
        else:
            print("\nYou chose to exit.Restarting....\n")
            break

def main():
    while True:
        city,month,day = get_filters()
        df = load_data(city,month,day)
        time_stats(df)
        station_stats(df)
        trip_duration_starts(df)
        user_stats(df)
        while True:
            rdata = input("\nWould you like to view raw data: enter 'yes' to view data or 'no' to exit\n").lower()
            if rdata != "yes":
                break
            else:
                display_data(df)
                break
        restart = input('\nWould you like to start from the beginning? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
