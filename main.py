from works.webscrapper import NewsScrapper
import sqlite3

database_file_path = './newsdb.db'

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


if __name__ == '__main__':
    # SQLLite3 데이터베이스 준비
    print(f'[main] connect database : {database_file_path}')
    conn = sqlite3.connect(database=database_file_path)
    c = conn.cursor()

    # 필요 테이블 생성
    print(f'[main] create table : jobs, news')
    c.execute(create_jobs_sql)
    c.execute(create_news_sql)

    # 최신 Job ID 생성
    last_job_id = c.execute(
        'SELECT jobid FROM jobs ORDER BY jobid DESC LIMIT 1').fetchone()
    current_job_id = 1 if last_job_id is None else int(last_job_id[0]) + 1
    print(f'[main] current job id : {current_job_id}')

    # 스크래퍼 생성 및 데이터 수집
    scrapper = NewsScrapper(keyword='마이데이터', maxpages=20, debug_mode=True)

    try:
        c.execute('INSERT INTO jobs (jobid, keyword) VALUES (?, ?)',
                  (current_job_id, scrapper.keyword))

        for item in scrapper.gather():
            data = item['title'], item['summary'], item['press'], item['link'], current_job_id
            c.execute(
                'INSERT INTO news(title, summary, press, link, jobid) VALUES (?, ?, ?, ?, ?)', data)

        c.execute('UPDATE jobs SET starttime = ?, endtime = ? WHERE jobid = ?',
                  (scrapper.start, scrapper.end, current_job_id))
    except Exception as e:
        conn.rollback()
        print(f'[main] insert job and news error : {e}')
    else:
        conn.commit()
    finally:
        scrapper = None

    print(f'[main] top 10 press list with search keyworrd: {scrapper.keyword}')
    c.execute(top_10_press_sql)
    for r in c.fetchall():
        print(f'\t{r[0]} : {r[1]} - {r[2]} 건')

    print(f'[main] close database : {database_file_path}')
    conn.close()
