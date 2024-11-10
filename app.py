from flask import Flask, request, render_template
import psycopg2

app = Flask(__name__)


# Kết nối đến cơ sở dữ liệu PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='haizdank0302'
    )
    return conn
categories_dict = {
    "_ban_doc": "Bạn đọc",
    "_bat_dong_san": "Bất động sản",
    "_cong_nghe": "Công nghệ",
    "_dien_dan": "Diễn đàn",
    "_cong_doan": "Công đoàn",
    "_du_lich": "Du lịch",
    "_gia_dinh_hon_nhan": "Gia đình hôn nhân",
    "_giao_duc": "Giáo dục",
    "_kinh_doanh": "Kinh doanh",
    "_lao_dong_cuoi_tuan": "Lao động cuối tuần",
    "_lao_dong_doi_song": "Lao động đời sống",
    "_lao_dong_xuan": "Lao động xuân",
    "_luu_tru": "Lưu trữ",
    "_media": "Media",
    "_nguoi_viet_tu_te": "Người Việt tử tế",
    "_phap_luat": "Pháp luật",
    "_phong_su": "Phóng sự",
    "_phong_su_dieu_tra": "Phóng sự điều tra", 
    "_quy_tlv": "Quỹ TLV",
    "_so_tay_kinh_te": "Sổ tay kinh tế",
    "_su_kien_binh_luan": "Sự kiện bình luận",
    "_suc_khoe": "Sức khỏe",
    "_tam_long_vang": "Tấm lòng vàng",
    "_tan_man_chuyen_doc_duong": "Tản mạn chuyện dọc đường",
    "_the_gioi": "Thế giới",
    "_the_thao": "Thể thao",
    "_thoi_su": "Thời sự",
    "_thong_tin_doanh_nghiep": "Thông tin doanh nghiệp",
    "_thong_tin_tien_ich": "Thông tin tiện ích", 
    "_tin_bai_lien_quan":"Tin bài liên quan", 
  	"tin_bai_noi_bat":"Tin bài nổi bật", 
  	"tin_bai_xem_them":"Tin bài xem thêm", 
  	"tin_dia_phuong":"Tin địa phương", 
  	"tinhoatdong":"Tin hoạt động", 
  	"tintucvieclam":"Tin tức việc làm", 
  	"vanhoagiaitri":"Văn hóa giải trí", 
  	"video":"Video", 
  	"xahoi":"Xã hội", 
  	"xeplus":"Xe Plus"
}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<category>', methods=['GET', 'POST'])
def manage_category(category):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        # Thêm mới bài viết
        url = request.form['url']
        title = request.form['title']
        summary = request.form['summary']
        content = request.form['content']
        date = request.form['date']
        author = request.form['author']
        tags = request.form['tags']
        cur.execute(f"""
            INSERT INTO vietnamnews (url, title, summary, content, date, author, category, tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (url, title, summary, content, date, author, categories_dict.get(category), tags))
        
        conn.commit()

    
    # Lấy danh sách bài viết từ bảng con theo category
    cur.execute(f"SELECT * FROM vietnamnews{category};")
    articles = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('manage_category.html', articles=articles, category=category)

@app.route('/delete/<category>', methods=['POST', 'GET'])
def delete_article(category):
    url = request.form['url']
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        cur.execute(f"""DELETE FROM vietnamnews WHERE url=%s;""", (url,))
    
        conn.commit()

    cur.execute(f"SELECT * FROM vietnamnews{category};")
    articles = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('manage_category.html', articles=articles)

@app.route('/get/<category>', methods=['GET'])
def get_a_news(category):
    url = request.args.get('url')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM vietnamnews{category} WHERE url=%s""", (url,))
    articles = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('get_a_news.html', articles=articles) 
    
@app.route('/update/<category>', methods=['PUT', 'GET'])
def update_article(category):
    if request.method == 'PUT':
        print("Received PUT request")
        url = request.form['url']
        title = request.form['title']
        summary = request.form['summary']
        content = request.form['content']
        date = request.form['date']
        author = request.form['author']
        tags = request.form['tags']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE vietnamnews
            SET title=%s, summary=%s, content=%s, date=%s, author=%s, tags=%s
            WHERE url=%s;
        """, (title, summary, content, date, author, url, tags))
        conn.commit()
        cur.close()
        conn.close()

        return 'Article updated successfully', 200

    # Handle GET request
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM vietnamnews{category};")
    articles = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('manage_category.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)