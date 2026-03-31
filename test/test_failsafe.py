import pytest
import time
from failsafe import FailsafeManager

def test_cpu_threshold_instant_normal():
    """Test that CPU under 95% returns NORMAL."""
    manager = FailsafeManager(cpu_threshold=95.0, duration=5.0)
    is_dangerous, reason = manager.check_system(cpu=50.0, temp=40.0)
    assert is_dangerous is False
    assert "NORMAL" in reason

def test_cpu_threshold_warning_period():
    """Test that CPU > 95% triggers a warning but NOT a failsafe immediately."""
    manager = FailsafeManager(cpu_threshold=95.0, duration=5.0)
    
    # First check
    is_dangerous, reason = manager.check_system(cpu=99.0, temp=40.0)
    assert is_dangerous is False
    assert "WARNING" in reason

def test_cpu_threshold_trigger_after_duration():
    """Test that CPU > 95% triggers failsafe after 5 seconds."""
    manager = FailsafeManager(cpu_threshold=95.0, duration=1.0) # Using 1s for fast test
    
    # Start the timer
    manager.check_system(cpu=99.0, temp=40.0)
    
    # Wait for the duration to pass
    time.sleep(1.1)
    
    is_dangerous, reason = manager.check_system(cpu=99.0, temp=40.0)
    assert is_dangerous is True
    assert "CRITICAL CPU" in reason

def test_temp_threshold_instant_trigger():
    """Test that high temperature triggers failsafe immediately."""
    manager = FailsafeManager(temp_threshold=75.0)
    is_dangerous, reason = manager.check_system(cpu=10.0, temp=80.0)
    assert is_dangerous is True
    assert "CRITICAL TEMP" in reason