import unittest
from producer.simulate_data import generate_sensor_data

class TestGenerateSensorData(unittest.TestCase):
    def test_structure(self):
        data = generate_sensor_data()
        self.assertIn("sensor_id", data)
        self.assertIn("timestamp", data)
        self.assertIn("location", data)
        self.assertIn("measures", data)
        self.assertIsInstance(data["measures"], dict)

    def test_anomalies(self):
        anomalies = 0
        for _ in range(100):
            data = generate_sensor_data()
            if len(data["measures"]) < 4 or any(not isinstance(v, (int, float)) for v in data["measures"].values()):
                anomalies += 1
        self.assertGreater(anomalies, 0)

if __name__ == "__main__":
    unittest.main()
