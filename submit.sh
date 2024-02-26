#!/bin/bash

if hash condor_submit 2>/dev/null
then

HOME="/lhome/ext/iiia021/iiia0211"
ROOT_DIR="$HOME/cmsa-rs"
EXECUTABLE="$ROOT_DIR/cmsa"
LOG_DIR="$HOME/log/cmsa-rs/$n-cmsa-$gen-$tb"
DATA_DIR="$ROOT_DIR/data"
POOL_DIR="$DATA_DIR/pmf_$n"

mkdir -p $LOG_DIR
mkdir -p $POOL_DIR
STDOUT=$POOL_DIR/$filename.stdout
STDERR=$POOL_DIR/$filename.stderr
STDLOG=$POOL_DIR/$filename.stdlog

tmpfile=$(mktemp)
condor_submit 1> $tmpfile <<EOF
universe = vanilla
stream_output = True
stream_error = True
executable = $EXECUTABLE
arguments = -i $POOL_DIR/$i.csv -s $seed -b $tb -g $gen $args
log = $STDLOG
output = $STDOUT
error = $STDERR
getenv = true
priority = $priority
queue
EOF

elif hash sbatch 2>/dev/null
then

USER=$(whoami)
BEEGFS="/mnt/beegfs/iiia/$USER"
ROOT_DIR="$BEEGFS/DPP"
EXECUTABLE="$ROOT_DIR/problem.py"
LOG_DIR="$ROOT_DIR"

mkdir -p $LOG_DIR
STDOUT=$LOG_DIR/results.stdout
STDERR=$LOG_DIR/results.stderr

tmpfile=$(mktemp)
sbatch 1> $tmpfile <<EOF
#!/bin/bash
#SBATCH --job-name=CA-$g-$b
#SBATCH --partition=general
#SBATCH --time=10:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

#SBATCH --output=$STDOUT
#SBATCH --error=$STDERR
echo python3 $EXECUTABLE -g $g -b $b -s $s -f $filename
srun python3 $EXECUTABLE -g $g -b $b -s $s -f $filename 1> $STDOUT 2> $STDERR
RET=\$?
exit \$RET
EOF

else

USER=$(whoami)
ROOT_DIR="/home/roger/Desktop/doctorat/github/ExMIP"
#ROOT_DIR="/home/roger/Desktop/Roger/github/ExMIP"
PROBLEM_DIR="$ROOT_DIR/CA"
EXECUTABLE="$PROBLEM_DIR/problem.py"
LOG_DIR="$PROBLEM_DIR/results"

mkdir -p $LOG_DIR
mkdir -p $LOG_DIR/$g-$b
STDOUT=$LOG_DIR/$g-$b/$filename.stdout
STDERR=$LOG_DIR/$g-$b/$filename.stderr
STDLOG=$LOG_DIR/$g-$b/$filename.stdlog


tmpfile=$(mktemp)
echo "python3 $EXECUTABLE"
python3 $EXECUTABLE > $STDOUT 2> $STDERR


fi