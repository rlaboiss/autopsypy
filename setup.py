# Copyright (C) 2023 Rafael Laboissière
#
# This file is part of autopsypy
#
# autopsypy is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# autopsypy is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with Foobar. If not, see <https://www.gnu.org/licenses/>.

from setuptools import setup

setup(
    name="autopsypy",
    version="0.1.3",
    description="Automate PsychoPy experiments",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Rafael Laboissière",
    author_email="rafael@laboissiere.net",
    license="GPL-3+",
    url="https://github.com/rlaboiss/autopsypy",
    project_urls={
        "ChangeLog": "https://github.com/rlaboiss/autopsypy/blob/main/CHANGELOG.md",
        "Tracker": "https://github.com/rlaboiss/autopsypy/issues",
    },
    package_dir={"": "src"},
    py_modules=["autopsypy"],
)
