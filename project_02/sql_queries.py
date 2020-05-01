import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

LOG_DATA = config.get('S3', 'LOG_DATA')
SONG_DATA = config.get('S3', 'SONG_DATA')
LOG_JSONPATH = config.get('S3', 'LOG_JSONPATH')
IAM_ROLE_ARN = config.get("IAM_ROLE", "ARN")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
        CREATE TABLE IF NOT EXISTS staging_events(
        artist VARCHAR,
        auth VARCHAR,
        first_name VARCHAR,
        gender CHAR(1),
        item_session INT,
        last_name VARCHAR,
        length FLOAT,
        level VARCHAR,
        location VARCHAR,
        method VARCHAR,
        page VARCHAR,
        registration FLOAT,
        session_id INT,
        song VARCHAR,
        status INT,
        ts BIGINT,
        user_agent VARCHAR,
        user_id INT);
""")

staging_songs_table_create = ("""
        CREATE  TABLE IF NOT EXISTS staging_songs
        (num_songs INT,
        artist_id VARCHAR,
        artist_latitude FLOAT,
        artist_longitude FLOAT,
        artist_location VARCHAR,
        artist_name VARCHAR,
        song_id VARCHAR,
        title VARCHAR,
        duration FLOAT,
        year INT);
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays
    (songplay_id INT PRIMARY KEY, 
    start_time TIMESTAMP NOT NULL, 
    user_id INT NOT NULL, 
    level VARCHAR, 
    song_id VARCHAR, 
    artist_id VARCHAR, 
    session_id INT, 
    location VARCHAR, 
    user_agent VARCHAR);
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users
    (user_id INT PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL, 
    gender CHAR(1), 
    level VARCHAR
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs
    (song_id VARCHAR PRIMARY KEY, 
    title VARCHAR NOT NULL, 
    artist_id VARCHAR NOT NULL, 
    year INT, 
    duration FLOAT
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists
    (artist_id VARCHAR PRIMARY KEY, 
    name VARCHAR NOT NULL, 
    location VARCHAR, 
    latitude FLOAT, 
    longitude FLOAT
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time
    (start_time TIMESTAMP PRIMARY KEY, 
    hour INT, 
    day INT, 
    week INT, 
    month INT, 
    year INT, 
    weekday VARCHAR
    );
""")

# STAGING TABLES

staging_events_copy = (f"""
    copy staging_events 
    from {LOG_DATA}
    region 'eu-central-1'
    iam_role {IAM_ROLE_ARN}
    json {LOG_JSONPATH};
""")

staging_songs_copy = (f"""
    copy staging_songs 
    from {SONG_DATA}
    region 'eu-central-1'
    iam_role {IAM_ROLE_ARN}
    json 'auto';
""").format()

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplay(
        start_time, 
        user_id, 
        level, 
        song_id, 
        artist_id, 
        session_id, 
        location, 
        user_agent)
    SELECT  timestamp 'epoch' + e.ts/1000 * interval '1 second' as start_time, 
            e.user_id, 
            e.level, 
            s.song_id, 
            s.artist_id, 
            e.session_id, 
            e.location, 
            e.user_agent
    FROM staging_events e, staging_songs s
    WHERE e.page = 'NextSong' AND
          e.song =s.title AND
          e.artist = s.artist_name AND
          e.length = s.duration
""")


user_table_insert = ("""
    INSERT INTO users(
        user_id, 
        first_name, 
        last_name, 
        gender, 
        level)
    SELECT distinct  user_id, 
                     first_name, 
                     last_name, 
                     gender, 
                     level
    FROM staging_events
    WHERE page = 'NextSong'
""")


song_table_insert = ("""
    INSERT INTO songs(
        song_id, 
        title, 
        artist_id, 
        year, 
        duration)
        SELECT song_id, 
               title, 
               artist_id, 
               year, 
               duration
        FROM staging_songs
        WHERE song_id IS NOT NULL
""")

artist_table_insert = ("""
    INSERT INTO artist(
        artist_id, 
        name, 
        location, 
        latitude, 
        longitude)
    SELECT distinct artist_id, 
                    artist_name, 
                    artist_location , 
                    artist_latitude, 
                    artist_longitude 
    FROM staging_songs
    WHERE artist_id IS NOT NULL
""")

time_table_insert = ("""
    INSERT INTO time(
        start_time, 
        hour, 
        day, 
        week, 
        month, 
        year, 
        weekDay)
    SELECT start_time, 
           extract(hour from start_time), 
           extract(day from start_time),
           extract(week from start_time), 
           extract(month from start_time),
           extract(year from start_time), 
           extract(dayofweek from start_time)
    FROM songplay
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
