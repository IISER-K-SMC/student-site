#!/bin/sh

echo "Starting Dev Setup"

tmux new-window ". venv/bin/activate;
				 . loadenv.sh;
				 uvicorn --reload --reload-dir server/ server:app;"
tmux split-window -dh -c "frontend/" "npm run dev"
tmux rename-window "Runners"
