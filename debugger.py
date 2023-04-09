def counter(debug=True):
    """Calculate and print the process time of a function, including sleeping times."""
    def check_debug_option(func):
        @functools.wraps(func)
        def count_process_time(*args, **kwargs):
            time1 = time.perf_counter()
            value = func(*args, **kwargs)
            time2 = time.perf_counter()
            if debug:
                print(f"[Process--function({func.__name__})]({round(time2 - time1, 3)} secs)")
            return value
        return count_process_time
    return check_debug_option


def start_and_exit_sign(debug=True):
    """Print when a function start and exit dynamically in your terminal."""
    def check_debug_option(func):
        @functools.wraps(func)
        def mark_start_and_exit(*args, **kwargs):
            if debug:
                print(f"########Start({func.__name__})########")
            value = func(*args, **kwargs)
            if debug:
                print(f"########Exit({func.__name__})########")
            return value
        return mark_start_and_exit
    return check_debug_option
