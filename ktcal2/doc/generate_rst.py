# -*- coding: utf-8 -*-

"""
ktcal2: 
"""

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

import sys
import os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))
base_path = os.getcwd()
sys.path.insert(0, base_path)
root_path = os.path.abspath(os.path.join(os.getcwd(), "../../."))
readme_file = os.path.join(os.getcwd(), "../../../.", "README.rst")
index_file_names = []
for root, dirs, files in os.walk(root_path):
    # Looking for .py files and packages
    if any(x.endswith(".py") for x in files) and any("__init__.py" in x for x in files):

        for f in files:
            if "__init__" in f or not f.endswith(".py"):
                continue

            f = os.path.join(root, f)
            # Create .rst files
            file_name = f.replace(root_path, "").replace(".py", "").replace(os.path.sep, ".")[1:]
            rst_file = "%s.rst" % os.path.join(base_path, file_name)

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

            index_file_names.append(file_name)

# Rewrite index.rst
with open(os.path.join(base_path, "index.rst"), "w") as f:

    # Readme
    f.write("Readme\n^^^^^^\n\n")
    with open(readme_file, "rU") as readme:
        for l in readme.readlines():
            f.write(l)

    # API
    f.write("\nAPI\n^^^^^^^^^^^^^\n\n")
    f.write("Content: \n\n\n")
    f.write(".. toctree::\n\n")
    for index in index_file_names:
        f.write("    %s <%s>\n" % (index.replace("_", " "), index))

    f.write("""\nIndices and tables
^^^^^^^^^^^^^^^^^^

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
""")
