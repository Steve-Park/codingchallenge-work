from works.scrapper import NewsScrapper
import sqlite3
import datetime

database_file_path = './newsdb.db'

create_sql = '''
    CREATE TABLE IF NOT EXISTS news (
        id              INTEGER     PRIMARY KEY     AUTOINCREMENT,
        title           TEXT,
        summary         TEXT,
        press           TEXT,
        link            TEXT,
        gatherdate      TEXT
    )'''.strip()

top_10_press_sql = '''
    SELECT press, COUNT(press) AS news_count
    FROM news
    GROUP BY press
    ORDER BY COUNT(press) DESC
    LIMIT 10
    '''.strip()


if __name__ == '__main__':
    today = datetime.date.today().strftime('%Y-%m-%d')

    # SQLLite3 데이터베이스 준비
    print(f'[main] connect database : {database_file_path}')
    conn = sqlite3.connect(database=database_file_path)
    c = conn.cursor()

    # 테이블 생성
    print(f'[main] create table : news')
    c.execute(create_sql)

    # 스크래퍼 생성 및 데이터 수집
    scrapper = NewsScrapper(keyword='마이데이터', maxpages=20, debug_mode=True)
    # scrapper = NewsScrapper(keyword='python', maxpages=20, debug_mode=True)

    try:
        for item in scrapper.gather():
            data = item['title'], item['summary'], item['press'], item['link'], today
            c.execute(
                'INSERT INTO news(title, summary, press, link, gatherdate) VALUES (?, ?, ?, ?, ?)', data)
    except Exception as e:
        conn.rollback()
        print(f'[main] error {e}')
        print(type(e))
    else:
        conn.commit()

    print(f'[main] top 10 press list with search keyworrd: {scrapper.keyword}')
    c.execute(top_10_press_sql)
    for r in c.fetchall():
        print(f'\t{r[0]} - {r[1]} 건')

    print(f'[main] close database : {database_file_path}')
    conn.close()
