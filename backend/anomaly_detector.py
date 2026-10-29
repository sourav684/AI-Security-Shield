import numpy as np
from sklearn.ensemble import IsolationForest

class OTAnomalyDetector:
    def __init__(self):
        # Isolation Forest is an unsupervised algorithm suitable for rare OT attacks
        self.model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
        self.is_trained = False

    def train_baseline(self):
        # Normal Traffic Feature Baseline: [Packet_Length (Bytes), Function_Code, Interval_Ms]
        # Normal Modbus: Read Holding Registers (FC=3), Length ~12 bytes, Interval ~1000ms
        normal_data = np.random.normal(loc=[12, 3, 1000], scale=[1, 0, 50], size=(500, 3))
        self.model.fit(normal_data)
        self.is_trained = True
        print("[+] ML Baseline Model Trained on Normal OT Traffic Baseline.")

    def predict_risk(self, packet_features):
        """
        packet_features: [length, function_code, interval_ms]
        Returns: (status_label, risk_score, recommended_action)
        """
        if not self.is_trained:
            self.train_baseline()
            
        # decision_function outputs negative scores for anomalies
        score = float(self.model.decision_function([packet_features])[0])
        
        # Risk Classification Logic based on score thresholds
        if score < -0.20:
            return "CRITICAL_ATTACK", score, "AUTOMATIC_THROTTLING"
        elif score < -0.05:
            return "SUSPICIOUS_ANOMALY", score, "SOC_ALERT"
        else:
            return "NORMAL", score, "NO_ACTION"

# Global Singleton Instance for backend consumption
detector = OTAnomalyDetector()
detector.train_baseline()