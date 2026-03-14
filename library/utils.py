import os
import sys


def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and Nuitka onefile
    """
    if hasattr(sys, "_nuitka_onefile_temp_dir"):
        base_path = sys._nuitka_onefile_temp_dir  # nuitka
    else:
        base_path = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )  # source

    return os.path.join(base_path, relative_path)
