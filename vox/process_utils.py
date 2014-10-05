from multiprocessing import Process


def spawn_daemon_process(fn, call_args=(), call_kw=None):
    call_kw = call_kw or {}

    process = Process(target=fn, args=call_args, kwargs=call_kw)
    process.daemon = True
    process.start()

    return process
