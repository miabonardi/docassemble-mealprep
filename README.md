# Meal Prep – a general UI platform for CLI-based Python script tools

## Authors

- Laurynas Keturakis, <laurynas.keturakis@gmail.com>
- Mia Bonardi, <mia.e.bonardi@gmail.com>

## Demo

Try it out at: apps.uiforcli.com

## **Disclaimer: Proof of Concept**

This is ~~a 3-day rage-coded project~~ an early concept exploration that in order to work makes many assumptions about the underlying scripts.

Things will break and might look odd.

**Known caveats:**
- The tool assumes that the script is written in Python and uses `argparse` library for parsing command line arguments.
- Some scripts that use multi-word arguments will break.
- The tool assumes the repository name is the package binary name.

## Description

Meal Prep aims to bridge the gap between OSINT researchers and tool builders. A lot of the useful tools produced by the OSINT community are CLI-based, which makes them inaccessible to many non-technical researchers. Meal Prep is a platform that automatically creates simple UIs for these scripts, flattening the learning curve and making them more accessible to a wider audience. It automatically ingests all Python-based CLI repositories on Bellingcat's GitHub organization, parses the required command flags and arguments, and renders a simple form-based UI flow that a researcher can input data into. The tool then generates the final command with the data prefiled, and provides simple instructions how to run it in the Google Colab tool (that has Python runtime preinstalled).

## How it works

Meal Prep is built on Docassemble: a Python-based open-source platform for building guided interviews (usually used in legal practice for gathering evidence).

The Meal Prep package is a simple Docassemble interview with a couple of custom Python modules that do the heavy lifting of parsing the GitHub repositories and generating the interview question fields. The interview is then hosted on a Docassemble server, and the final command is generated and displayed to the user.

## Further explorations

- **Providing guidance for script developers**: a major benefit of Meal Prep is that it enables extracting helpful information directly from code without requiring the developer to write a lot of additional documentation. The more structured and uniform the scripts are, the easier it is to generate useful UIs. One example would be to recommend using `argparse` library for parsing command line arguments, as it is much easier to extract information from it than from a custom parser or environment variables. Another, encourage using a convention for naming the arguments, e.g. `--input-file` instead of `--input_file` or `--inputFile`, as well as adding helpful descriptions to the arguments and inside the code.

- **Replace with a more lightweight platform**: while Docassemble is a powerful tool for building guided interviews and was helpful in quickly prototyping this flow, it is a bit of an overkill for this use case. It is a heavy package that requires a lot of resources to run, somewhat specialized training, and is not very easy to deploy. A more lightweight and easier to maintain solution would be to use either a general web framework (Flask, Django, SvelteKit, NextJS etc.) or an open-source internal tool builder (Appsmith, Tooljet). Although arguably they would be slightly more work to build initially, they would be much easier to maintain, deploy, and cheap to host on something like a serverless platform.
- **Investigate directly running the Python scripts**. A slightly more ambitious approach would be to directly run the Python scripts from the UI using something like the Pyodide library. The Pyodide library executes the Python code directly in the browser, saving the maintainers from most of the hassle of maintaining a full-fledged Python runtime on the host server.

## Other

With inspiration and source code from the Suffolk LIT Lab's Document Assembly Line Project, specifically the [ALDashboard]( https://github.com/SuffolkLITLab/docassemble-ALDashboard)
