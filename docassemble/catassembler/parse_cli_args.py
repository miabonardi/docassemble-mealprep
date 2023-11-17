import requests
import zipfile
import io
import ast

def fetch_and_extract_root_file(repo):
	"""
	Fetches the root file from the given repo and returns the contents.
	"""

	archive_url = repo["archive_url"]

	response = requests.get(archive_url) # TODO: reuse the github client from other modules

	if response.status_code != 200:
		raise Exception("Error fetching repo archive")
	
	virtual_file = io.BytesIO(response.content)

	root_file = {}

	with zipfile.ZipFile(virtual_file) as zf:
		for filename in zf.namelist():
			if filename.endswith(".py"):
				with zf.open(filename) as py_file:
					file_contents = py_file.read().decode("utf-8")

					contents_array = file_contents.split("\n")

					for idx, line in enumerate(contents_array):
						if "argparse" in line:
							print(f"Found: {contents_array[idx]} on line {idx + 1} in file {filename}")
							root_file = {
								"filename": filename,
								"contents": file_contents
							}
							break

	return root_file

def get_cli_args(repo):
	"""
	Gets the CLI arguments from the given repo and returns them as a list.

	They should be presented in the following format:
	[
		{
			"name": "arg_name",
			"help_text": "arg_help_text"
		}
	]
	"""

	root_file_contents = fetch_and_extract_root_file(repo)
	root_file_tree = ast.parse(root_file_contents["contents"])

	all_extracted_args = []

	for node in ast.walk(root_file_tree):
		if isinstance(node, ast.Call):
			if isinstance(node.func, ast.Attribute):
				if node.func.attr == "add_argument" and node.func.value.id == "parser":
					extracted_arg = {}

					for arg in node.args:
						if isinstance(arg, ast.Str):
							extracted_arg["name"] = arg.s.replace("--", "")
					for keyword in node.keywords:
						if keyword.arg == "help":
							extracted_arg["help_text"] = keyword.value.s
					all_extracted_args.append(extracted_arg)

	return all_extracted_args
