import os, subprocess

owner = os.environ["OWNER"]
out = subprocess.run(
    ["gh", "api", f"orgs/{owner}/repos?per_page=100&type=public", "--paginate",
     "--jq", r'.[] | [.name, .html_url, .archived] | @tsv'],
    capture_output=True, text=True, check=True).stdout

repos = []
for line in out.splitlines():
    name, url, archived = line.split("\t")
    if name == ".github" or archived == "true":
        continue
    repos.append((name, url))
repos.sort(key=lambda r: r[0].lower())

rows = ["| Group repository | Link |", "|---|---|"]
rows += [f"| {n} | [Open]({u}) |" for n, u in repos]
table = "\n".join(rows)

path = "profile/README.md"
text = open(path, encoding="utf-8").read()
start, end = "<!-- GROUPS:START -->", "<!-- GROUPS:END -->"
a, b = text.index(start) + len(start), text.index(end)
new = text[:a] + "\n" + table + "\n" + text[b:]
if new != text:
    open(path, "w", encoding="utf-8", newline="\n").write(new)
