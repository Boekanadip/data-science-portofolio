# resave_calibrator.py
import joblib
import sys
import pickle

# Import class dari lokasi yang benar
from app.models import TemperatureScaler

# Cara 1: Coba load dengan mengabaikan error (risky)
try:
    with open("assets/calibrator.pkl", "rb") as f:
        # Baca data mentah
        old_data = pickle.load(f)
    print("Berhasil load calibrator lama")
    
    # Re-save dengan import yang benar
    joblib.dump(old_data, "assets/calibrator_new.pkl")
    print("✅ Berhasil re-save ke calibrator_new.pkl")
    
except Exception as e:
    print(f"❌ Gagal load: {e}")
    print("\n🔧 Membuat calibrator baru...")
    
    # Buat calibrator baru jika gagal
    new_calibrator = TemperatureScaler()
    joblib.dump(new_calibrator, "assets/calibrator_new.pkl")
    print("✅ Berhasil membuat calibrator_new.pkl")