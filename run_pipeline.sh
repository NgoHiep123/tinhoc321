#!/bin/bash
# ============================================
# PIPELINE TỰ ĐỘNG - XÂY DỰNG HỆ THỐNG
# Chạy file này để build KG -> KNN -> PPR
# Dành cho Linux/Mac
# ============================================

echo "========================================"
echo "  HỆ THỐNG HỖ TRỢ GIÁO VIÊN THCS"
echo "  Pipeline: KG -> KNN -> PPR"
echo "========================================"
echo ""

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Không tìm thấy Python! Vui lòng cài đặt Python 3.8+"
    exit 1
fi

echo "[OK] Python đã được cài đặt"
echo ""

# Kiểm tra dependencies
echo "[1/5] Kiểm tra dependencies..."
if ! python3 -c "import rdflib" &> /dev/null; then
    echo "[WARNING] Chưa cài đặt dependencies!"
    echo "[INFO] Đang cài đặt..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Cài đặt thất bại!"
        exit 1
    fi
fi
echo "[OK] Dependencies đã sẵn sàng"
echo ""

# Bước 1: Xây dựng KG
echo "[2/5] Xây dựng Knowledge Graph..."
cd KG_Design
python3 build_kg_grade7.py
if [ $? -ne 0 ]; then
    echo "[ERROR] Xây dựng KG thất bại!"
    cd ..
    exit 1
fi
cd ..
echo "[OK] Knowledge Graph đã được xây dựng (kg_grade7.ttl)"
echo ""

# Bước 2: Chạy KNN
echo "[3/5] Chạy thuật toán KNN (phát hiện học sinh yếu)..."
cd ML_Algorithms
python3 knn_student_analysis.py
if [ $? -ne 0 ]; then
    echo "[ERROR] KNN thất bại!"
    cd ..
    exit 1
fi
cd ..
echo "[OK] KNN hoàn thành (kg_grade7_with_knn.ttl)"
echo ""

# Bước 3: Chạy PPR
echo "[4/5] Chạy thuật toán PPR (gợi ý bài học)..."
cd ML_Algorithms
python3 ppr_recommendation.py
if [ $? -ne 0 ]; then
    echo "[ERROR] PPR thất bại!"
    cd ..
    exit 1
fi
cd ..
echo "[OK] PPR hoàn thành (kg_grade7_with_ppr.ttl)"
echo ""

# Bước 4: Truy vấn demo
echo "[5/5] Truy vấn Knowledge Graph (demo)..."
cd KG_Design
python3 query_kg.py
cd ..
echo ""

echo "========================================"
echo "  PIPELINE HOÀN THÀNH THÀNH CÔNG!"
echo "========================================"
echo ""
echo "[INFO] Các file output:"
echo "  - KG_Design/kg_grade7.ttl"
echo "  - KG_Design/kg_grade7_with_knn.ttl"
echo "  - KG_Design/kg_grade7_with_ppr.ttl"
echo ""
echo "[NEXT] Bước tiếp theo:"
echo "  1. Mở dashboard: Web_Teacher/dashboard.html"
echo "  2. Hoặc xem hướng dẫn: HUONG_DAN_TIEP_THEO.md"
echo ""

