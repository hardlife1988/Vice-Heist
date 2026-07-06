#!/bin/bash
echo "Building Vice Heist for Stake Engine..."
mkdir -p dist
cp index.html game.js style.css dist/ 2>/dev/null || true
cp -r math/library/publish_files/* dist/ 2>/dev/null || true
echo "✅ Build complete! Upload the 'dist' folder to Stake."
ls dist
