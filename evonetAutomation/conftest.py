# content of conftest.py
import pytest
import os
import sys


# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def pytest_addoption(parser):  # 新增加了解析的参数  envirs
    parser.addoption(
        "--envirs", action="store", default="test", help="my option: test or staging or pro"
    )


@pytest.fixture
def envirs(request):
    return request.config.getoption("--envirs")


# .多个标签;每次加了标签需要这里配置下，不然日志中会warning
# 在conftest.py添加如下代码，直接拷贝过去，把标签名改成你自己的就行了

def pytest_configure(config):
    marker_list = ["smoke", "funcs", ]  # 标签名集合
    for markers in marker_list:
        config.addinivalue_line(
            "markers", markers
        )

# pytest --s.html=./report/report.s.html --self-contained-s.html
