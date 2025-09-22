#!/bin/bash
set -e

sudo chown -R ec2-user:ec2-user /home/ec2-user/Mood_Companion_Lambda
chmod -R 755 /home/ec2-user/Mood_Companion_Lambda

# Kill old Streamlit processes
pkill -f streamlit || true

# Start Streamlit app
nohup /home/ec2-user/.local/bin/streamlit run /home/ec2-user/Mood_Companion_Lambda/app.py \
  --server.port 8501 --server.address 0.0.0.0 > /home/ec2-user/Mood_Companion_Lambda/streamlit.log 2>&1 &

