SHELL := cmd.exe
.SHELLFLAGS := /C

.PHONY: check-port show-pid kill-pid ollama-serve diagnose

check-port:
	netstat -ano | findstr :11434

show-pid:
	@if "$(PID)"=="" ( \
		echo Please provide PID. Example: make show-pid PID=1234 && exit /b 1 \
	) else ( \
		tasklist /FI "PID eq $(PID)" \
	)

kill-pid:
	@if "$(PID)"=="" ( \
		echo Please provide PID. Example: make kill-pid PID=1234 && exit /b 1 \
	) else ( \
		taskkill /PID $(PID) /F \
	)

serve:
	ollama serve

tags:
	@curl http://127.0.0.1:11434/api/tags

diagnose:
	@echo Checking port 11434...
	netstat -ano | findstr :11434
	@echo.
	@echo If needed, run:
	@echo   make show-pid PID=1234
	@echo   make kill-pid PID=1234
	@echo   make ollama-serve

claude:
	@ollama run glm-4.7-flash

gemma3:
	@ollama run gemma3:270m

phi3:
	@ollama run phi3

gpt:
	@ollama run gpt-oss

install:
	pip install uv
	uv pip install -r requirements.txt

nb:
	@jupyter notebook --port 12000