import unittest
from aerocrypt.protocol import parse_telemetry, parse_link_metrics, parse_security_status

class TelemetryProtocolTests(unittest.TestCase):
    def test_base_telemetry(self):
        p=parse_telemetry("2276,28.49,918.08,0.004,0.058,1.009,0.42,1.06,0.08")
        self.assertEqual(p.packet,2276); self.assertAlmostEqual(p.temperature_c,28.49)
        self.assertAlmostEqual(p.pressure_hpa,918.08); self.assertIsNone(p.latitude)
    def test_extended_gps(self):
        p=parse_telemetry("42,27.5,1001.2,.1,.2,.9,1.1,1.2,1.3,12.971599,77.594566,8,.9")
        self.assertAlmostEqual(p.latitude,12.971599); self.assertEqual(p.satellites,8)
    def test_invalid_count(self):
        with self.assertRaises(ValueError): parse_telemetry("1,2,3")
    def test_invalid_numeric(self):
        with self.assertRaises(ValueError): parse_telemetry("x,28,918,0,0,1,0,0,0")
    def test_link(self):
        m=parse_link_metrics("AEROCRYPT_LINK,RSSI=-43,SNR=5.25")
        self.assertEqual(m.rssi_dbm,-43); self.assertAlmostEqual(m.snr_db,5.25)
    def test_security_verified(self):
        self.assertTrue(parse_security_status("AEROCRYPT_SECURITY:VERIFIED,PACKET=7")["verified"])
    def test_security_rejected(self):
        self.assertFalse(parse_security_status("AEROCRYPT_SECURITY:REJECTED:GCM_AUTH_FAILED")["verified"])

if __name__ == "__main__": unittest.main()
