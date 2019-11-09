import twint

from twitpol import config, utils, db


def make_config(hide_output=True, get_location=True):
    c = twint.Config()
    c.Pandas = True
    c.Location = get_location
    c.Pandas_clean = True
    c.Hide_output = hide_output
    return c


def get_queries():
    with (config.DATA / 'queries' / 'twitter_search_queries.txt').open() as f:
        queries = []
        for line in f:
            queries.append(line.split(': '))


def run_search(c):
    twint.run.Search(c)
    return twint.storage.panda.Tweets_df


def write_df_to_db(df, engine=None):
    if engine is None:
        engine = db.get_db_engine()
    df.to_sql(config.DB_SETTINGS.database, con=engine, if_exists='append')


def main():
    c = make_config()
    queries = get_queries()
    engine = db.get_db_engine()
    for query in queries:
        name, q = query
        c.Search = q
        for d1, d2 in utils.date_range(config.start_date, config.end_date, day_step=1):
            c.Since = d1
            c.Until = d2

            df_tweets = run_search(c)
            df_tweets['name'] = name


            write_df_to_db(df_tweets, engine)

            n_tweets = len(df_tweets)
            print(f'{name} - {d1} - Downloaded {n_tweets} tweets.')

if __name__ == '__main__':
    main()
