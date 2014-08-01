# -*- coding: utf-8 -*-

from __future__ import print_function

__license__ = '''Copyright (c) cr0hn - cr0hn<-at->cr0hn.com (@ggdaniel) All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of cr0hn nor the names of its contributors may be used
       to endorse or promote products derived from this software without
       specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.'''

__author__ = 'cr0hn - cr0hn<-at->cr0hn.com (@ggdaniel)'


import os

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------

# Do not process this files/dirs
EXCLUDE_FILES_OR_DIRS = ["bin"]

# Readme file
README_FILE_PATH = os.path.abspath(os.path.join(os.getcwd(), "../../.", "README.rst"))

# Documentation base directory
DOC_DIR = os.path.join(os.getcwd(), "source")

# Source code base directory
PROJECT_DIR = os.path.abspath(os.path.join(os.path.join(os.getcwd()), "../."))


# --------------------------------------------------------------------------
# Find all .py files
# --------------------------------------------------------------------------

# Files found
found_py_files = []

for root, dirs, files in os.walk(PROJECT_DIR):

    # Looking for .py files and packages, not explicitly excluded
    if any(x.endswith(".py") for x in files) and \
            any("__init__.py" in x for x in files) and \
            any(x not in EXCLUDE_FILES_OR_DIRS for x in files):

        # Process each file
        for f in files:
            print(f)
            if "__init__" in f or not f.endswith(".py"):  # Not process not .py or package maker files
                continue

            # Get and clean filename path
            f = os.path.join(root, f)
            file_name = f.replace(PROJECT_DIR, "").replace(".py", "").replace(os.path.sep, ".")[1:]

            # Get path in doc path
            rst_file = "%s.rst" % os.path.join(DOC_DIR, file_name)

            # Write info
            with open(rst_file, "w") as fw:
                content = (
                              "%s\n"
                              "%s\n\n"
                              ".. automodule:: %s\n"
                              "   :members:\n"
                              "   :special-members:\n"
                          ) % (
                              file_name,
                              ("-" * len(file_name)),
                              file_name
                          )

                fw.write(content)

            # Get file path to add in index.rst
            found_py_files.append(file_name)

# --------------------------------------------------------------------------
# Create index.rst
# --------------------------------------------------------------------------
with open(os.path.join(DOC_DIR, "index.rst"), "w") as f:

    # Readme
    f.write("Readme\n^^^^^^\n\n")
    with open(README_FILE_PATH, "rU") as readme:
        for l in readme.readlines():
            f.write(l)

    # API
    f.write("\nAPI\n^^^^^^^^^^^^^\n\n")
    f.write("Content: \n\n\n")
    f.write(".. toctree::\n\n")
    for index in found_py_files:
        f.write("    %s <%s>\n" % (index.replace("_", " "), index))

    # Index
    f.write("""\nIndices and tables
^^^^^^^^^^^^^^^^^^

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
""")
