import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Prompts the user to select a city, month, and day to filter the bikeshare data.
    Returns the selections as strings for later use in data analysis.
    """

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input("Choose a city (Chicago, New York City, Washington): ").strip().lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please enter: Chicago, New York City, or Washington.")

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Choose a month (January - June) or 'all': ").strip().lower()
        if month in months:
            break
        else:
            print("Invalid input. Please enter a valid month or 'all'.")

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Choose a day of week or 'all': ").strip().lower()
        if day in days:
            break
        else:
            print("Invalid input. Please enter a valid day of the week or 'all'.")

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        city (str): Name of the city
        month (str): Name of the month or 'all'
        day (str): Name of the day of the week or 'all'

    Returns:
        DataFrame: Filtered bikeshare data
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months.index(month) + 1
        df = df[df['month'] == month_num]

    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day.lower()]

    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df (DataFrame): bikeshare data filtered by city, month, and day

    Returns:
        None
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print("Most Common Month:", df['month'].mode()[0])
    print("Most Common Day of Week:", df['day_of_week'].mode()[0])

    common_hour = df['Start Time'].dt.hour.mode()[0]
    formatted_hour = pd.to_datetime(str(common_hour), format='%H').strftime('%I %p')
    print("Most Common Start Hour:", formatted_hour)

    def get_time_of_day(hour):
        if 5 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 17:
            return 'Afternoon'
        elif 17 <= hour < 21:
            return 'Evening'
        else:
            return 'Night'

    df['hour'] = df['Start Time'].dt.hour
    df['Time of Day'] = df['hour'].apply(get_time_of_day)
    busiest_category = df['Time of Day'].mode()[0]
    print("Busiest Time of Day:", busiest_category)

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip combinations.

    Args:
        df (DataFrame): bikeshare data

    Returns:
        None
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print("Most Common Start Station:", df['Start Station'].mode()[0])
    print("Most Common End Station:", df['End Station'].mode()[0])

    df['Trip Combo'] = df['Start Station'] + " → " + df['End Station']
    print("Most Common Trip:", df['Trip Combo'].mode()[0])

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def trip_duration_stats(df):
    """
    Displays statistics on total, average, longest, and shortest trip durations.

    Args:
        df (DataFrame): bikeshare data

    Returns:
        None
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    def format_duration(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}h {minutes}m {secs}s"

    total_duration = df['Trip Duration'].sum()
    average_duration = df['Trip Duration'].mean()
    print("Total Travel Time:", format_duration(total_duration))
    print("Average Travel Time:", format_duration(average_duration))

    max_duration = df['Trip Duration'].max()
    longest_trip = df[df['Trip Duration'] == max_duration].iloc[0]
    print("\nLongest Trip Duration:", format_duration(max_duration))
    if longest_trip['Start Station'] == longest_trip['End Station']:
        print("  Trip (round-trip):", longest_trip['Start Station'])
    else:
        print("  From:", longest_trip['Start Station'])
        print("  To:", longest_trip['End Station'])

    min_duration = df['Trip Duration'].min()
    shortest_trip = df[df['Trip Duration'] == min_duration].iloc[0]
    print("\nShortest Trip Duration:", format_duration(min_duration))
    if shortest_trip['Start Station'] == shortest_trip['End Station']:
        print("  Trip (round-trip):", shortest_trip['Start Station'])
    else:
        print("  From:", shortest_trip['Start Station'])
        print("  To:", shortest_trip['End Station'])

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def user_stats(df):
    """
    Displays statistics on bikeshare users: user types, gender, and birth years.

    Args:
        df (DataFrame): bikeshare data

    Returns:
        None
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("User Types:\n", df['User Type'].value_counts(), "\n")

    if 'Gender' in df.columns:
        print("Gender Counts:\n", df['Gender'].value_counts(), "\n")
    else:
        print("Gender data not available for this city.\n")

    if 'Birth Year' in df.columns:
        print("Earliest Birth Year:", int(df['Birth Year'].min()))
        print("Most Recent Birth Year:", int(df['Birth Year'].max()))
        print("Most Common Birth Year:", int(df['Birth Year'].mode()[0]))
    else:
        print("Birth Year data not available for this city.")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def popular_trip_by_time_group(df):
    """
    Displays the most popular trip combination for each time-of-day category.

    Args:
        df (DataFrame): bikeshare data

    Returns:
        None
    """
    print('\nCalculating Most Popular Trip by Time of Day...\n')
    start_time = time.time()

    df['hour'] = df['Start Time'].dt.hour
    df['Trip Combo'] = df['Start Station'] + " → " + df['End Station']

    def get_time_of_day(hour):
        if 5 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 17:
            return 'Afternoon'
        elif 17 <= hour < 21:
            return 'Evening'
        else:
            return 'Night'

    df['Time of Day'] = df['hour'].apply(get_time_of_day)
    time_groups = df.groupby('Time of Day')

    for group_name, group_df in time_groups:
        most_common_trip = group_df['Trip Combo'].mode()[0]
        print(f"{group_name}: {most_common_trip}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def display_raw_data(df):
    """
    Displays raw data 5 rows at a time upon user request.

    Args:
        df (DataFrame): bikeshare data

    Returns:
        None
    """
    i = 0
    show = input("\nWould you like to see 5 lines of raw data? (yes/no): ").strip().lower()
    while show == 'yes':
        print(df.iloc[i:i+5])
        i += 5
        show = input("Would you like to see 5 more lines? (yes/no): ").strip().lower()

def main():
    """
    Runs the interactive bikeshare data analysis program.
    Allows users to filter data and see descriptive statistics.

    Returns:
        None
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        popular_trip_by_time_group(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no: ').strip().lower()
        if restart != 'yes':
            print("Thanks for exploring US Bikeshare data!")
            print("""
                __o
              _ \\<_  
             (_)/(_)  Keep riding!
            """)
            break

if __name__ == "__main__":
    main()
