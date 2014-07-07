# coding=utf-8
import os, time, cProfile
from django.conf import settings

try:
    PROFILER_LOG_BASE = settings.PROFILER_LOG_BASE
    USE_PROFILER = settings.USE_PROFILER
except:
    PROFILER_LOG_BASE = settings.SITE_ROOT
    USE_PROFILER = False


def profile(log_file):
    """Profile some callable.

    This decorator uses the cProfiler to profile some callable (like
    a view function or method) and dumps the profile data somewhere sensible
    for later processing and examination.

    It takes one argument, the profile log name. If it's a relative path, it
    places it under the PROFILER_LOG_BASE. It also inserts a time stamp into the
    file name, such that 'my_view.prof' become 'my_view-20100211T170321.prof',
    where the time stamp is in UTC. This makes it easy to run and compare
    multiple trials.
    """

    if not os.path.isabs(log_file):
        log_file = os.path.join(PROFILER_LOG_BASE, log_file)

    def _outer(f):
        def _inner(*args, **kwargs):
            # Add a timestamp to the profile output when the callable
            # is actually called.

            final_log_file = log_file + "-" + time.strftime("%Y%m%dT%H%M%S", time.gmtime()) + '.prof'

            prof = cProfile.Profile()
            try:
                res = prof.runcall(f, *args, **kwargs)
            finally:
                prof.dump_stats(final_log_file)
            return res
        return _inner

    def _empty(f):
        return f

    return _outer if USE_PROFILER else _empty
