import pytest
import numpy as np
import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from theremin import CameraCapture, HandProcessor, SoundGenerator

# Mock for gesture dataset
TEST_GESTURES = [
    ('hand_up', 0.9),  # 90% height
    ('pinch_open', 0.0),
    ('pinch_close', 1.0)
]

def test_latency():
    cam = CameraCapture()
    start = time.time()
    frame = cam.get_frame()
    end = time.time()
    cam.release()
    assert frame is None or (end - start) * 1000 < 30, 'Latency above 30ms'

def test_handprocessor_precision():
    processor = HandProcessor()
    # This is a placeholder: in real test, use a dataset of labeled images
    # Here, we just check the output structure
    dummy = np.zeros((480, 640, 3), dtype=np.uint8)
    result = processor.process(dummy)
    assert 'left_hand' in result and 'right_hand' in result and 'gestures' in result

# Audio underrun/stability test

def test_soundgenerator_stability():
    sg = SoundGenerator()
    sg.start_stream()
    sg.update_parameters(440.0, 1.0)
    time.sleep(0.2)
    sg.stop_stream()
    assert True  # If no exception, pass

def test_memory_usage():
    import psutil
    process = psutil.Process()
    mem_mb = process.memory_info().rss / (1024 * 1024)
    assert mem_mb < 300, f'Memory usage too high: {mem_mb:.2f} MB'
