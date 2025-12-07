#!/bin/bash
set -e

NUM_ITERATIONS=10
OUT_DIR="out/attempt1"
MOVEMENT=("momentum" "static" "random")
ENVIRONMENT=("env1" "env2" "env3" "env4" "env5")
COOPERATE_PERCENTS=("0.0" "0.25" "0.5" "0.75" "1.0")
UPDATE_INTERVALS=("5" "10" "20")
STRATEGY_INERTIA=("1.0" "2.0" "5.0" "10.0")
FPS=10
SPAWN_PERCENT=0.75
FRAMES=false
VIDEO=false

# Calculate total number of simulations
total_sims=$((${#MOVEMENT[@]} * ${#ENVIRONMENT[@]} * ${#COOPERATE_PERCENTS[@]} * ${#UPDATE_INTERVALS[@]} * ${#STRATEGY_INERTIA[@]} * NUM_ITERATIONS))
current_sim=0

# Track timing
start_time=$(date +%s)

echo "Total simulations to run: $total_sims"
echo ""

for movement in "${MOVEMENT[@]}"; do
    echo "Running simulations for movement strategy: $movement"
    for env in "${ENVIRONMENT[@]}"; do
        echo " Running simulations for environment: $env"
        for cooperate_percent in "${COOPERATE_PERCENTS[@]}"; do
            echo "  Running simulations for cooperate percent: $cooperate_percent"
            for update_interval in "${UPDATE_INTERVALS[@]}"; do
                echo "   Using update interval: $update_interval"
                for strategy_inertia in "${STRATEGY_INERTIA[@]}"; do
                    echo "    Using strategy inertia: $strategy_inertia"
                    for i in $(seq 0 $((NUM_ITERATIONS - 1))); do
                        current_sim=$((current_sim + 1))
                        
                        # Calculate progress and ETA
                        current_time=$(date +%s)
                        elapsed=$((current_time - start_time))
                        
                        if [ $current_sim -gt 1 ]; then
                            remaining_sims=$((total_sims - current_sim + 1))
                            avg_time_per_sim=$(echo "$elapsed / ($current_sim - 1)" | bc -l)
                            eta_seconds=$(echo "$avg_time_per_sim * $remaining_sims" | bc -l)
                            eta_seconds=${eta_seconds%.*}  # convert float → int
                            
                            # Format ETA as HH:MM:SS
                            eta_hours=$((eta_seconds / 3600))
                            eta_minutes=$(((eta_seconds % 3600) / 60))
                            eta_secs=$((eta_seconds % 60))
                            eta_formatted=$(printf "%02d:%02d:%02d" $eta_hours $eta_minutes $eta_secs)
                            
                            # Calculate completion time (macOS compatible)
                            completion_timestamp=$((current_time + eta_seconds))
                            completion_time=$(date -j -f "%s" "$completion_timestamp" +"%Y-%m-%d %H:%M:%S" 2>/dev/null || date -r "$completion_timestamp" +"%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "N/A")
                            progress=$((current_sim * 100 / total_sims))
                            
                            echo "     [$current_sim/$total_sims - ${progress}%] ETA: $eta_formatted | Complete by: $completion_time"
                        else
                            echo "     [$current_sim/$total_sims] Calculating ETA..."
                        fi
                        
                        echo "     Starting iteration $i..."
                        current_dir="$OUT_DIR/$movement/$env/coop_$cooperate_percent/update_$update_interval/strat_inertia_$strategy_inertia/iter_$i"
                        
                        if [ -d "$current_dir" ]; then
                            echo "     Skipping iteration $i (output directory already exists)."
                            continue
                        fi
                        
                        mkdir -p "$current_dir"
                        current_dir=$(realpath "$current_dir")
                        seed=$RANDOM

                        video_args=""
                        if [ "$VIDEO" = "true" ]; then
                            video_args="--video=$current_dir/out.mp4 \
  --fps=$FPS \
  --frames=true"
                        fi

                        cmd="python main.py \\
  --env=$env \\
  --movement=$movement \\
  --json=$current_dir/out.json \\
  $video_args \\
  --spawn_percent=$SPAWN_PERCENT \\
  --cooperate_percent=$cooperate_percent \\
  --update_interval=$update_interval \\
  --strategy_inertia=$strategy_inertia \\
  --seed=$seed \\
  --verbose=true > $current_dir/out.log "
                        
                        echo "$cmd" >> "$current_dir/command.sh"
                        chmod +x "$current_dir/command.sh"
                        eval "$cmd"
                        
                        echo "     Completed iteration $i."
                    done
                done
            done
        done
    done
done

# Format total time
total_seconds=$(($(date +%s) - start_time))
total_hours=$((total_seconds / 3600))
total_minutes=$(((total_seconds % 3600) / 60))
total_secs=$((total_seconds % 60))
total_time=$(printf "%02d:%02d:%02d" $total_hours $total_minutes $total_secs)

echo ""
echo "All iterations complete!"
echo "Total time: $total_time"
