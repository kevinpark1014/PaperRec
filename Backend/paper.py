import csv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database import SessionLocal
from models import Paper


# CSV 파일을 읽고 데이터베이스에 데이터 삽입하는 함수
def insert_data_from_csv(csv_file_path):
    db = SessionLocal()
    try:
        with open(csv_file_path, "r") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                if row["citation_count"] == "" or row["reference_count"] == "" or row["published_year"] == "":
                    continue
                paper = Paper(
                    paper_id=row["paper_id"],
                    title=row["title"],
                    updated_year=int(row["updated_year"]),
                    categories=row["categories"],
                    journals=row["journals"],
                    author=row["author"],
                    keyword=row["keyword"],
                    citation_count=int(float(row["citation_count"])),
                    reference_count=int(float(row["reference_count"])),
                    published_year=int(float(row["published_year"]))
                )
                db.add(paper)
            db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# CSV 파일 경로
csv_file_path = "/home/kev/Backend/databases_2023-04.csv"  # 실제 파일 경로로 변경하세요.

# CSV 파일을 읽고 데이터베이스에 데이터 삽입
insert_data_from_csv(csv_file_path)