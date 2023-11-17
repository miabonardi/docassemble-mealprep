import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')

def find_package_data(where='.', package='', exclude=standard_exclude, exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

setup(name='docassemble.catassembler',
      version='0.0.1',
      description=('UI4CLI submission for Bellingcat Hackathon Fall 2023.'),
      long_description="# Meal Prep – a general UI platform for CLI-based Python script tools\r\n\r\n## Authors\r\n\r\n- Laurynas Keturakis, <laurynas.keturakis@gmail.com>\r\n- Mia Bonardi, <mia.e.bonardi@gmail.com>\r\n\r\n## Demo\r\n\r\nTry it out at: [apps.uiforcli.com](https://apps.uiforcli.com)\r\n\r\n## **Disclaimer: Proof of Concept**\r\n\r\nThis is ~~a 3-day rage-coded project~~ an early concept exploration that in order to work makes many assumptions about the underlying scripts.\r\n\r\nThings will break and might look odd.\r\n\r\n**Known caveats:**\r\n- The tool assumes that the script is written in Python and uses `argparse` library for parsing command line arguments.\r\n- Some scripts that use multi-word arguments will break.\r\n- The tool assumes the repository name is the package binary name.\r\n\r\n## Description\r\n\r\nMeal Prep aims to bridge the gap between OSINT researchers and tool builders. A lot of the useful tools produced by the OSINT community are CLI-based, which makes them inaccessible to many non-technical researchers. Meal Prep is a platform that automatically creates simple UIs for these scripts, flattening the learning curve and making them more accessible to a wider audience. It automatically ingests all Python-based CLI repositories on Bellingcat's GitHub organization, parses the required command flags and arguments, and renders a simple form-based UI flow that a researcher can input data into. The tool then generates the final command with the data prefiled, and provides simple instructions how to run it in the Google Colab tool (that has Python runtime preinstalled).\r\n\r\n## How it works\r\n\r\nMeal Prep is built on Docassemble: a Python-based open-source platform for building guided interviews (usually used by legal professionals in A2J space).\r\n\r\nThe Meal Prep package is a simple Docassemble interview with a couple of custom Python modules that do the heavy lifting of parsing the GitHub repositories and generating the interview question fields. The interview is then hosted on a Docassemble server, and the final command is generated and displayed to the user.\r\n\r\n## Further explorations\r\n\r\n- **Providing guidance for script developers**: a major benefit of Meal Prep is that it enables extracting helpful information directly from code without requiring the developer to write a lot of additional documentation. The more structured and uniform the scripts are, the easier it is to generate useful UIs. One example would be to recommend using `argparse` library for parsing command line arguments, as it is much easier to extract information from it than from a custom parser or environment variables. As another example, we encourage using a convention for naming the arguments, e.g. `--input-file` instead of `--input_file` or `--inputFile` or vice versa. Finally, we also recommend adding helpful descriptions to the arguments and inside the code.\r\n\r\n- **Replace with a more lightweight platform**: while Docassemble is a powerful tool for building guided interviews and was helpful in quickly prototyping this flow, it is a bit of an overkill for this use case. It is a heavy package that requires a lot of resources to run, somewhat specialized training, and is not very easy to deploy. A more lightweight and easier to maintain solution would be to use either a general web framework (Flask, Django, SvelteKit, NextJS etc.) or an open-source internal tool builder (Appsmith, Tooljet). Although arguably they would be slightly more work to build initially, they would be much easier to maintain, deploy, and cheap to host on something like a serverless platform.\r\n\r\n- **Investigate directly running the Python scripts**. A slightly more ambitious approach would be to directly run the Python scripts from the UI using something like the Pyodide library. The Pyodide library executes the Python code directly in the browser, saving the maintainers from most of the hassle of maintaining a full-fledged Python runtime on the host server.\r\n\r\n## Other\r\n\r\nWith inspiration and source code from the Suffolk LIT Lab's Document Assembly Line Project, specifically the [ALDashboard]( https://github.com/SuffolkLITLab/docassemble-ALDashboard).\r\n",
      long_description_content_type='text/markdown',
      author=' Laurynas Keturakis & Mia Bonardi',
      author_email='laurynas.keturakis@gmail.com',
      license='MIT License',
      url='https://apps.uiforcli.com',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=['PyGithub>=2.1.1'],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/catassembler/', package='docassemble.catassembler'),
     )

