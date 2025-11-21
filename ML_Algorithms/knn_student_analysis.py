"""
Thuật toán K-Nearest Neighbors (KNN)
Mục đích: Phát hiện học sinh yếu ở các chủ đề cụ thể
"""

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from rdflib import Graph, Namespace, Literal
from collections import defaultdict

EDU = Namespace("http://education.vn/ontology#")
DATA = Namespace("http://education.vn/data/")

# ============================================
# 1. THU THẬP DỮ LIỆU TỪ KG
# ============================================

def extract_student_features_from_kg(kg_file='../KG_Design/kg_grade7.ttl'):
    """
    Trích xuất vector đặc trưng của học sinh từ KG
    
    Vector đặc trưng cho mỗi học sinh ở mỗi chủ đề:
    - Điểm trung bình các bài kiểm tra thuộc chủ đề
    - Số bài đã làm
    - Tỷ lệ câu đúng trung bình
    - Thời gian làm bài trung bình
    """
    print("📊 Đang trích xuất dữ liệu từ Knowledge Graph...")
    
    g = Graph()
    g.parse(kg_file, format='turtle')
    g.bind("edu", EDU)
    g.bind("data", DATA)
    
    query = """
    PREFIX edu: <http://education.vn/ontology#>
    PREFIX data: <http://education.vn/data/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?student ?studentName ?lesson ?topic ?score ?duration
    WHERE {
        ?student a edu:Student .
        ?student edu:fullName ?studentName .
        
        ?result edu:hasResult ?student .
        ?result edu:forTest ?test .
        ?result edu:score ?score .
        
        OPTIONAL { ?result edu:duration ?duration . }
        
        # Liên kết test -> lesson -> topic
        ?test edu:hasQuestion ?question .
        ?question edu:belongsToLesson ?lesson .
        ?lesson edu:belongsToTopic ?topic .
        ?topic rdfs:label ?topicName .
    }
    """
    
    results = g.query(query)
    
    # Tổ chức dữ liệu
    data = []
    for row in results:
        data.append({
            'student': str(row.student),
            'student_name': str(row.studentName),
            'lesson': str(row.lesson),
            'topic': str(row.topic),
            'score': float(row.score),
            'duration': int(row.duration) if row.duration else 0
        })
    
    df = pd.DataFrame(data)
    
    if df.empty:
        print("⚠️  Không có dữ liệu kết quả. Sử dụng dữ liệu giả để demo.")
        return generate_sample_data()
    
    print(f"✅ Đã trích xuất {len(df)} bản ghi")
    return df

def generate_sample_data():
    """
    Tạo dữ liệu mẫu để demo thuật toán
    """
    np.random.seed(42)
    
    students = [f"Student_{i}" for i in range(1, 101)]
    topics = ['A', 'B', 'C', 'D', 'E']
    
    data = []
    for student in students:
        for topic in topics:
            # Tạo điểm ngẫu nhiên (một số học sinh yếu ở topic A)
            if topic == 'A' and np.random.rand() < 0.3:
                score = np.random.uniform(3, 5)  # Yếu
            else:
                score = np.random.uniform(5, 10)  # Trung bình - Khá
            
            data.append({
                'student': student,
                'student_name': student,
                'topic': f'topic_7{topic}',
                'score': score,
                'num_tests': np.random.randint(2, 5),
                'avg_duration': np.random.randint(300, 900)
            })
    
    return pd.DataFrame(data)

# ============================================
# 2. TIỀN XỬ LÝ DỮ LIỆU
# ============================================

def prepare_features(df):
    """
    Tạo vector đặc trưng cho KNN
    
    Features:
    - avg_score: Điểm trung bình
    - num_tests: Số bài kiểm tra đã làm
    - avg_duration: Thời gian làm bài trung bình (nếu có)
    
    Label:
    - weak (1): Yếu nếu avg_score < 5.0
    - not_weak (0): Không yếu nếu avg_score >= 5.0
    """
    print("🔧 Đang chuẩn bị vector đặc trưng...")
    
    # Tính toán features theo từng (student, topic)
    features = df.groupby(['student', 'student_name', 'topic']).agg({
        'score': ['mean', 'count', 'std'],
        'duration': 'mean'
    }).reset_index()
    
    features.columns = ['student', 'student_name', 'topic', 'avg_score', 'num_tests', 'std_score', 'avg_duration']
    
    # Điền giá trị NaN
    features['std_score'].fillna(0, inplace=True)
    features['avg_duration'].fillna(600, inplace=True)
    
    # Tạo nhãn: weak = 1 nếu avg_score < 5.0
    features['weak'] = (features['avg_score'] < 5.0).astype(int)
    
    print(f"✅ Đã chuẩn bị {len(features)} vector đặc trưng")
    print(f"   - Học sinh yếu: {features['weak'].sum()}")
    print(f"   - Học sinh không yếu: {(~features['weak'].astype(bool)).sum()}")
    
    return features

# ============================================
# 3. HUẤN LUYỆN MÔ HÌNH KNN
# ============================================

def train_knn_model(features, k=5):
    """
    Huấn luyện mô hình KNN
    
    Args:
        features: DataFrame chứa features và labels
        k: Số lượng hàng xóm gần nhất
    
    Returns:
        model: Mô hình KNN đã huấn luyện
        scaler: Scaler để chuẩn hóa dữ liệu
    """
    print(f"🤖 Đang huấn luyện mô hình KNN (k={k})...")
    
    # Chọn features
    X = features[['avg_score', 'num_tests', 'std_score', 'avg_duration']].values
    y = features['weak'].values
    
    # Chuẩn hóa
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Huấn luyện KNN
    model = KNeighborsClassifier(n_neighbors=k, weights='distance')
    model.fit(X_scaled, y)
    
    # Đánh giá trên tập huấn luyện
    accuracy = model.score(X_scaled, y)
    print(f"✅ Hoàn thành huấn luyện. Độ chính xác: {accuracy:.2%}")
    
    return model, scaler

# ============================================
# 4. DỰ ĐOÁN HỌC SINH YẾU
# ============================================

def predict_weak_students(features, model, scaler):
    """
    Dự đoán học sinh yếu ở từng chủ đề
    """
    print("🔮 Đang dự đoán học sinh yếu...")
    
    X = features[['avg_score', 'num_tests', 'std_score', 'avg_duration']].values
    X_scaled = scaler.transform(X)
    
    predictions = model.predict(X_scaled)
    probabilities = model.predict_proba(X_scaled)[:, 1]  # Xác suất yếu
    
    features['predicted_weak'] = predictions
    features['weak_probability'] = probabilities
    
    # Lọc học sinh yếu
    weak_students = features[features['predicted_weak'] == 1].copy()
    weak_students = weak_students.sort_values('weak_probability', ascending=False)
    
    print(f"✅ Tìm thấy {len(weak_students)} học sinh yếu")
    
    return weak_students

# ============================================
# 5. CẬP NHẬT KG VỚI KẾT QUẢ KNN
# ============================================

def update_kg_with_weak_students(weak_students, kg_file='../KG_Design/kg_grade7.ttl', output_file='../KG_Design/kg_grade7_with_knn.ttl'):
    """
    Thêm quan hệ weakInTopic vào KG
    """
    print("💾 Đang cập nhật Knowledge Graph...")
    
    g = Graph()
    g.parse(kg_file, format='turtle')
    g.bind("edu", EDU)
    g.bind("data", DATA)
    
    count = 0
    for _, row in weak_students.iterrows():
        student_uri = DATA[row['student'].split('/')[-1]]
        topic_uri = DATA[row['topic'].split('/')[-1]]
        
        g.add((student_uri, EDU.weakInTopic, topic_uri))
        count += 1
    
    # Lưu KG mới
    g.serialize(destination=output_file, format='turtle')
    
    print(f"✅ Đã thêm {count} quan hệ weakInTopic vào KG")
    print(f"💾 KG mới được lưu tại: {output_file}")
    
    return g

# ============================================
# 6. BÁO CÁO KẾT QUẢ
# ============================================

def generate_report(weak_students):
    """
    Tạo báo cáo cho giáo viên
    """
    print("\n" + "=" * 80)
    print("📊 BÁO CÁO HỌC SINH YẾU THEO CHỦ ĐỀ")
    print("=" * 80)
    
    # Thống kê theo chủ đề
    topic_stats = weak_students.groupby('topic').agg({
        'student': 'count',
        'avg_score': 'mean',
        'weak_probability': 'mean'
    }).round(2)
    
    topic_stats.columns = ['Số học sinh yếu', 'Điểm TB', 'Xác suất TB']
    
    print("\n🔍 Thống kê theo chủ đề:")
    print(topic_stats)
    
    # Top học sinh cần can thiệp
    print("\n⚠️  TOP 10 học sinh cần can thiệp ưu tiên:")
    print("-" * 80)
    top_10 = weak_students.head(10)[['student_name', 'topic', 'avg_score', 'weak_probability']]
    for i, (_, row) in enumerate(top_10.iterrows(), 1):
        topic_id = row['topic'].split('_')[-1]
        print(f"{i:2d}. {row['student_name']:20s} | Chủ đề {topic_id} | Điểm: {row['avg_score']:.1f} | Xác suất: {row['weak_probability']:.0%}")
    
    print("\n" + "=" * 80)

# ============================================
# 7. MAIN FUNCTION
# ============================================

def main():
    """Hàm chính"""
    print("=" * 80)
    print("🚀 THUẬT TOÁN KNN - PHÁT HIỆN HỌC SINH YẾU")
    print("=" * 80)
    
    # 1. Trích xuất dữ liệu
    df = extract_student_features_from_kg()
    
    # 2. Chuẩn bị features
    features = prepare_features(df)
    
    # 3. Huấn luyện KNN
    model, scaler = train_knn_model(features, k=5)
    
    # 4. Dự đoán
    weak_students = predict_weak_students(features, model, scaler)
    
    # 5. Cập nhật KG
    update_kg_with_weak_students(weak_students)
    
    # 6. Báo cáo
    generate_report(weak_students)
    
    print("\n✅ HOÀN THÀNH!")

if __name__ == '__main__':
    main()

