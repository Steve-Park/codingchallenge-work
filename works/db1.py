import sqlite3

create_jobs_sql = '''
    CREATE TABLE IF NOT EXISTS jobs (
        jobid           INTEGER     PRIMARY KEY,
        keyword         TEXT,
        starttime       TEXT,
        endtime         TEXT
    )'''.strip()

create_news_sql = '''
    CREATE TABLE IF NOT EXISTS news (
        newsid          INTEGER     PRIMARY KEY     AUTOINCREMENT,
        title           TEXT,
        summary         TEXT,
        press           TEXT,
        link            TEXT,
        jobid           INTEGER,
        FOREIGN KEY(jobid) REFERENCES jobs(jobid)
    )'''.strip()

top_10_press_sql = '''
    SELECT jobs.keyword, news.press, COUNT(news.title) AS cnt
    FROM jobs JOIN news
    ON jobs.jobid = news.jobid 
    GROUP BY jobs.keyword, news.press
    ORDER BY COUNT(news.title) DESC, jobs.keyword ASC
    LIMIT 10;'''.strip()


def initalize(database_file_path):
    # SQLLite3 데이터베이스 준비
    print(f'\t[db] connect database : {database_file_path}')
    conn = sqlite3.connect(database=database_file_path)
    c = conn.cursor()

    # 필요 테이블 생성
    print(f'\t[db] create table : jobs, news')
    c.execute(create_jobs_sql)
    c.execute(create_news_sql)

    conn.commit()

    return conn


def get_last_job_id(conn: sqlite3.Connection):
    c = conn.cursor()
    last_job_id = c.execute(
        'SELECT jobid FROM jobs ORDER BY jobid DESC LIMIT 1').fetchone()

    return 0 if last_job_id is None else int(last_job_id[0])


def create_job_info(conn: sqlite3.Connection, job_id: int, keyword: str):
    c = conn.cursor()
    c.execute('INSERT INTO jobs (jobid, keyword) VALUES (?, ?)',
              (job_id, keyword))
    conn.commit()


def create_news_info(conn: sqlite3.Connection, job_id, news: list):
    c = conn.cursor()

    for item in news:
        c.execute('INSERT INTO news(title, summary, press, link, jobid) VALUES (?, ?, ?, ?, ?)',
                  (item['title'], item['summary'], item['press'], item['link'], job_id))

    conn.commit()


def update_job_info(conn: sqlite3.Connection, job_id, start_time, end_time):
    c = conn.cursor()
    c.execute('UPDATE jobs SET starttime = ?, endtime = ? WHERE jobid = ?',
              (start_time, end_time, job_id))
    conn.commit()


def get_top10_press(conn: sqlite3.Connection):
    c = conn.cursor()
    return c.execute(top_10_press_sql).fetchall()


def finalize(conn: sqlite3.Connection):
    conn.close()
