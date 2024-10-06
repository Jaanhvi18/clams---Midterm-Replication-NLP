#!/bin/bash

echo "Running prepdata.py..."
python prepdata.py

if [ $? -eq 0 ]; then
    echo "prepdata.py completed successfully."
    
    echo "Running find_roi.py..."
    python find_roi.py
    
    if [ $? -eq 0 ]; then
        echo "find_roi.py completed successfully."
    else
        echo "Error: find_roi.py encountered an issue."
        exit 1
    fi
else
    echo "Error: prepdata.py encountered an issue."
    exit 1
fi
