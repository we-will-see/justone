.PHONY: help health tracker-open notebook-open

help:
	@echo "Available targets:"
	@echo "  make health        # print a quick repository health report"
	@echo "  make tracker-open  # show docs/TRACKER.md"
	@echo "  make notebook-open # print notebook metadata summary"

health:
	python3 scripts/repo_health.py

tracker-open:
	sed -n '1,220p' docs/TRACKER.md

notebook-open:
	python3 -c "import json; nb=json.load(open('notebooks/agent.ipynb')); print('Notebook: notebooks/agent.ipynb'); print('Cells:', len(nb.get('cells', []))); print('Kernel:', nb.get('metadata', {}).get('kernelspec', {}).get('display_name'))"
