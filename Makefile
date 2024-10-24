.PHONY: run stop

# Variables to hold the PIDs of the background processes
MAIN_PID = main_pid
CRON_PID = cron_pid

# Rule to run both Python scripts in the background
run:
	@echo "Starting discordbot.py and cron.py in background..."
	@python cmd/discordbot.py & echo $$! > $(MAIN_PID)
	@python cmd/cron.py & echo $$! > $(CRON_PID)
	@trap 'make stop' SIGINT; \
	while [ -e $(MAIN_PID) ] && kill -0 `cat $(MAIN_PID)` 2>/dev/null && \
	      [ -e $(CRON_PID) ] && kill -0 `cat $(CRON_PID)` 2>/dev/null; do \
	    sleep 1; \
	done

# Rule to stop both processes by killing them
stop:
	@echo "Stopping both processes..."
	@if [ -f $(MAIN_PID) ]; then kill `cat $(MAIN_PID)` 2>/dev/null && echo "Stopped discordbot.py" || echo "discordbot.py already stopped"; rm -f $(MAIN_PID); fi
	@if [ -f $(CRON_PID) ]; then kill `cat $(CRON_PID)` 2>/dev/null && echo "Stopped cron.py" || echo "cron.py already stopped"; rm -f $(CRON_PID); fi
	@echo "Both processes stopped."
