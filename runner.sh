#!/bin/sh

echo "Starting Dev Setup"

tmux new-window ". venv/bin/activate;
				 . loadenv.sh;
				 cd backend; uvicorn --reload --reload-dir server/ server:app;"
tmux split-window -dh -c "frontend/" "npm run dev"
tmux rename-window "Runners"
