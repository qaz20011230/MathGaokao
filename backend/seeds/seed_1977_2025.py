import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.document import Document
from app.config import settings
from passlib.hash import bcrypt
from app.models.document import Admin
import hashlib
import os

period_map = {
    "1977": "1977_now",
    "1978": "1977_now",
    "1979": "1977_now",
}

province_map = {
    "全国卷": None,
}

def seed_documents():
    db = SessionLocal()

    md5_path = "/Users/leon/Eureka/1977—2025高考数学真题全编.pdf"
    if not os.path.exists(md5_path):
        print(f"Warning: {md5_path} not found, skipping file check")
        db.close()
        return

    md5_func = hashlib.md5()
    with open(md5_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5_func.update(chunk)
    file_md5 = md5_func.hexdigest()

    file_size = os.path.getsize(md5_path)

    years_info = [
        {"year": 1977, "title": "1977年全国高考数学试卷", "period": "1977_now", "doc_type": "other", "province": None, "exam_category": "通用"},
        {"year": 1978, "title": "1978年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1978, "title": "1978年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1979, "title": "1979年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1979, "title": "1979年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1980, "title": "1980年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1980, "title": "1980年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1981, "title": "1981年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1981, "title": "1981年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1982, "title": "1982年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1982, "title": "1982年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1983, "title": "1983年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1983, "title": "1983年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1984, "title": "1984年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1984, "title": "1984年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1985, "title": "1985年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1985, "title": "1985年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1986, "title": "1986年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1986, "title": "1986年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1987, "title": "1987年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1987, "title": "1987年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1988, "title": "1988年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1988, "title": "1988年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1989, "title": "1989年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1989, "title": "1989年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1990, "title": "1990年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1990, "title": "1990年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1991, "title": "1991年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1991, "title": "1991年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1992, "title": "1992年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1992, "title": "1992年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1993, "title": "1993年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1993, "title": "1993年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1994, "title": "1994年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1994, "title": "1994年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1995, "title": "1995年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1995, "title": "1995年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1996, "title": "1996年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1996, "title": "1996年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1997, "title": "1997年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1997, "title": "1997年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1998, "title": "1998年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1998, "title": "1998年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 1999, "title": "1999年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 1999, "title": "1999年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2000, "title": "2000年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2000, "title": "2000年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2001, "title": "2001年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2001, "title": "2001年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2002, "title": "2002年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2002, "title": "2002年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2003, "title": "2003年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2003, "title": "2003年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2004, "title": "2004年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2004, "title": "2004年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2005, "title": "2005年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2005, "title": "2005年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2006, "title": "2006年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2006, "title": "2006年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2007, "title": "2007年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2007, "title": "2007年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2008, "title": "2008年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2008, "title": "2008年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2009, "title": "2009年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2009, "title": "2009年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2010, "title": "2010年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2010, "title": "2010年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2011, "title": "2011年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2011, "title": "2011年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2012, "title": "2012年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2012, "title": "2012年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2013, "title": "2013年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2013, "title": "2013年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2014, "title": "2014年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2014, "title": "2014年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2015, "title": "2015年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2015, "title": "2015年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2016, "title": "2016年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2016, "title": "2016年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2017, "title": "2017年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2017, "title": "2017年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2018, "title": "2018年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2018, "title": "2018年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2019, "title": "2019年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2019, "title": "2019年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2020, "title": "2020年全国高考数学试卷(理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2020, "title": "2020年全国高考数学试卷(文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2021, "title": "2021年全国高考数学试卷(新高考Ⅰ卷)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "新高考"},
        {"year": 2021, "title": "2021年全国高考数学试卷(新高考Ⅱ卷)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "新高考"},
        {"year": 2021, "title": "2021年全国高考数学试卷(全国甲卷·理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2021, "title": "2021年全国高考数学试卷(全国甲卷·文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2021, "title": "2021年全国高考数学试卷(全国乙卷·理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2021, "title": "2021年全国高考数学试卷(全国乙卷·文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2022, "title": "2022年全国高考数学试卷(新高考Ⅰ卷)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "新高考"},
        {"year": 2022, "title": "2022年全国高考数学试卷(新高考Ⅱ卷)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "新高考"},
        {"year": 2022, "title": "2022年全国高考数学试卷(全国甲卷·理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2022, "title": "2022年全国高考数学试卷(全国甲卷·文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2022, "title": "2022年全国高考数学试卷(全国乙卷·理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2022, "title": "2022年全国高考数学试卷(全国乙卷·文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2023, "title": "2023年全国高考数学试卷(新高考Ⅰ卷)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "新高考"},
        {"year": 2023, "title": "2023年全国高考数学试卷(新高考Ⅱ卷)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "新高考"},
        {"year": 2023, "title": "2023年全国高考数学试卷(全国甲卷·理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2023, "title": "2023年全国高考数学试卷(全国甲卷·文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2023, "title": "2023年全国高考数学试卷(全国乙卷·理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2023, "title": "2023年全国高考数学试卷(全国乙卷·文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2024, "title": "2024年全国高考数学试卷(新高考Ⅰ卷)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "新高考"},
        {"year": 2024, "title": "2024年全国高考数学试卷(新高考Ⅱ卷)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "新高考"},
        {"year": 2024, "title": "2024年全国高考数学试卷(全国甲卷·理科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "理科"},
        {"year": 2024, "title": "2024年全国高考数学试卷(全国甲卷·文科)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "文科"},
        {"year": 2025, "title": "2025年全国高考数学试卷(新高考Ⅰ卷)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "新高考"},
        {"year": 2025, "title": "2025年全国高考数学试卷(新高考Ⅱ卷)", "period": "1977_now", "doc_type": "exam_paper", "province": None, "exam_category": "新高考"},
    ]

    dest_dir = "/Users/leon/Eureka/mathgaokao/data/documents/1977-2025"
    os.makedirs(dest_dir, exist_ok=True)

    import shutil
    dest_path = os.path.join(dest_dir, "1977—2025高考数学真题全编.pdf")
    shutil.copy2(md5_path, dest_path)

    for info in years_info:
        try:
            existing = db.query(Document).filter(
                Document.year == info["year"],
                Document.doc_type == info["doc_type"],
                Document.exam_category == info["exam_category"],
            ).first()

            if existing:
                continue

            doc = Document(
                title=info["title"],
                year=info["year"],
                period=info["period"],
                doc_type=info["doc_type"],
                province=info["province"],
                exam_category=info["exam_category"],
                file_path="1977-2025/1977—2025高考数学真题全编.pdf",
                file_format="pdf",
                file_size=file_size,
                file_md5=file_md5,
                is_published=1,
                source="mathgaokao.top 编纂",
                description=f"{info['year']}年高考数学试卷，收录于《1977—2025高考数学真题全编》",
            )
            db.add(doc)
        except Exception as e:
            db.rollback()
            print(f"Error inserting {info['title']}: {e}")

    db.commit()
    db.close()
    print(f"Seed complete. Inserted documents for 1977-2025.")


def seed_admin():
    db = SessionLocal()
    password_hash = bcrypt.hash(settings.admin_password)
    existing = db.query(Admin).filter(Admin.username == settings.admin_username).first()
    if not existing:
        admin = Admin(username=settings.admin_username, password_hash=password_hash)
        db.add(admin)
        db.commit()
        print(f"Admin user '{settings.admin_username}' created.")
    else:
        print(f"Admin user '{settings.admin_username}' already exists.")
    db.close()


if __name__ == "__main__":
    seed_admin()
    seed_documents()
