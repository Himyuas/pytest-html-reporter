import pytest
import time
import os

from _pytest.runner import pytest_runtest_setup
from _pytest.runner import pytest_runtest_teardown
from pytest_html_reporter.template import html_template

_total = _executed = 0
_pass = _fail = 0
_skip = _error = 0
_xpass = _xfail = 0
_current_error = ""
_suite_name = _test_name = None
_test_status = None
_test_start_time = None
_excution_time = _duration = 0
_test_metrics_content = _suite_metrics_content = ""
_previous_suite_name = "None"
_initial_trigger = True
_spass_tests = _sfail_tests = _sskip_tests = 0
_serror_tests = _sxfail_tests = _sxpass_tests = 0


def pytest_addoption(parser):
    group = parser.getgroup("report generator")
    group.addoption(
        "--html",
        action="store",
        dest="path",
        default=".",
        help="path to generate html report",
    )


def pytest_configure(config):
    path = config.getoption("path")

    config._html = HTMLReporter(path, config)
    config.pluginmanager.register(config._html)


class HTMLReporter:

    def __init__(self, path, config):
        self.path = path
        self.config = config

    def report_path(self):
        logfile = os.path.expanduser(os.path.expandvars(self.path))
        return os.path.abspath(logfile)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        yield

        report_file_name = "pytest_report.html"
        path = os.path.join(self.report_path(), report_file_name)
        live_logs_file = open(path, 'w')
        message = self.get_updated_template_text('https://i.imgur.com/OdZIPpg.png')
        live_logs_file.write(message)
        live_logs_file.close()


    def get_updated_template_text(self, logo_url):
        template_text = html_template()
        template_text = template_text.replace("__custom_logo__", logo_url)
        template_text = template_text.replace("__execution_time__", str(round(_excution_time, 2)))
        # template_text = template_text.replace("__executed_by__", str(platform.uname()[1]))
        # template_text = template_text.replace("__os_name__", str(platform.uname()[0]))
        # template_text = template_text.replace("__python_version__", str(sys.version.split(' ')[0]))
        # template_text = template_text.replace("__generated_date__", str(datetime.datetime.now().strftime("%b %d %Y, %H:%M")))
        template_text = template_text.replace("__total__", str(_total))
        template_text = template_text.replace("__executed__", str(_executed))
        template_text = template_text.replace("__pass__", str(_pass))
        template_text = template_text.replace("__fail__", str(_fail))
        template_text = template_text.replace("__skip__", str(_skip))
        # template_text = template_text.replace("__error__", str(_error))
        template_text = template_text.replace("__xpass__", str(_xpass))
        template_text = template_text.replace("__xfail__", str(_xfail))
        template_text = template_text.replace("__suite_metrics_row__", str(_suite_metrics_content))
        template_text = template_text.replace("__test_metrics_row__", str(_test_metrics_content))
        return template_text