import time
import datetime

def safe_ctime(timestamp=None):
    """
    Wrapper around time.ctime with input validation.
    Accepts a float/int timestamp or None.
    """
    try:
        if timestamp is None:
            # No argument: use current time
            return time.ctime()  # Uses localtime internally
        if not isinstance(timestamp, (int, float)):
            raise TypeError("timestamp must be int, float, or None")
        return time.ctime(timestamp)
    except (OverflowError, OSError, ValueError) as e:
        try:
            ts = dt.timestamp()
            st = time.localtime(ts)
            return st
        except:
            try:
                return time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
            except:
            # Handles timestamps out of supported system range
                return f"Invalid timestamp: {e}"

#print(safe_ctime())
