from works.wc1 import NewsScrapper
import works.db1 as db

database_file_path = './newsdb.db'

if __name__ == '__main__':
    # 데이터베이스 초기화
    conn = db.initalize(database_file_path=database_file_path)
    print(f'[main] initalize database : {database_file_path}')

    # 스크래퍼 생성 및 데이터 수집
    scrapper = NewsScrapper(keyword='마이데이터', maxpages=20, debug_mode=True)
    print(f'[main] initalize scrapper : {scrapper.keyword}')

    # 최신 Job ID 생성
    current_job_id = db.get_last_job_id(conn) + 1
    print(f'[main] current job id : {current_job_id}')

    try:
        db.create_job_info(conn, current_job_id, scrapper.keyword)
        db.create_news_info(conn, current_job_id, scrapper.gather())
        db.update_job_info(conn, current_job_id, scrapper.start, scrapper.end)
    except Exception as e:
        conn.rollback()
        print(f'[main] insert job and news error : {e}')

    print(f'[main] top 10 press list with search keyworrd: {scrapper.keyword}')
    for r in db.get_top10_press(conn):
        print(f'\t{r[0]} : {r[1]} - {r[2]} 건')

    scrapper = None
    db.finalize(conn)
    print(f'[main] finalize : {database_file_path}')
