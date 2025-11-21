@echo off
REM ============================================
REM PIPELINE TỰ ĐỘNG - XÂY DỰNG HỆ THỐNG
REM Chạy file này để build KG -> KNN -> PPR
REM ============================================

echo ========================================
echo   HE THONG HO TRO GIAO VIEN THCS
echo   Pipeline: KG -^> KNN -^> PPR
echo ========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Khong tim thay Python! Vui long cai dat Python 3.8+
    pause
    exit /b 1
)

echo [OK] Python da duoc cai dat
echo.

REM Kiểm tra dependencies
echo [1/5] Kiem tra dependencies...
pip show rdflib >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Chua cai dat dependencies!
    echo [INFO] Dang cai dat...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Cai dat that bai!
        pause
        exit /b 1
    )
)
echo [OK] Dependencies da san sang
echo.

REM Bước 1: Xây dựng KG
echo [2/5] Xay dung Knowledge Graph...
cd KG_Design
python build_kg_grade7.py
if errorlevel 1 (
    echo [ERROR] Xay dung KG that bai!
    cd ..
    pause
    exit /b 1
)
cd ..
echo [OK] Knowledge Graph da duoc xay dung (kg_grade7.ttl)
echo.

REM Bước 2: Chạy KNN
echo [3/5] Chay thuat toan KNN (phat hien hoc sinh yeu)...
cd ML_Algorithms
python knn_student_analysis.py
if errorlevel 1 (
    echo [ERROR] KNN that bai!
    cd ..
    pause
    exit /b 1
)
cd ..
echo [OK] KNN hoan thanh (kg_grade7_with_knn.ttl)
echo.

REM Bước 3: Chạy PPR
echo [4/5] Chay thuat toan PPR (goi y bai hoc)...
cd ML_Algorithms
python ppr_recommendation.py
if errorlevel 1 (
    echo [ERROR] PPR that bai!
    cd ..
    pause
    exit /b 1
)
cd ..
echo [OK] PPR hoan thanh (kg_grade7_with_ppr.ttl)
echo.

REM Bước 4: Truy vấn demo
echo [5/5] Truy van Knowledge Graph (demo)...
cd KG_Design
python query_kg.py
cd ..
echo.

echo ========================================
echo   PIPELINE HOAN THANH THANH CONG!
echo ========================================
echo.
echo [INFO] Cac file output:
echo   - KG_Design/kg_grade7.ttl
echo   - KG_Design/kg_grade7_with_knn.ttl
echo   - KG_Design/kg_grade7_with_ppr.ttl
echo.
echo [NEXT] Buoc tiep theo:
echo   1. Mo dashboard: Web_Teacher/dashboard.html
echo   2. Hoac xem huong dan: HUONG_DAN_TIEP_THEO.md
echo.

pause

