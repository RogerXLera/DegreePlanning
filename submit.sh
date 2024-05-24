#!/bin/bash

if hash sbatch 2>/dev/null
then

ROOT_DIR=$(pwd)
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

ROOT_DIR=$(pwd)
EXECUTABLE="$ROOT_DIR/problem.py"
LOG_DIR="$ROOT_DIR/results"

mkdir -p $LOG_DIR
mkdir -p $LOG_DIR/$g-$b
STDOUT=$LOG_DIR/$g-$b/$filename.stdout
STDERR=$LOG_DIR/$g-$b/$filename.stderr
STDLOG=$LOG_DIR/$g-$b/$filename.stdlog


tmpfile=$(mktemp)
echo "python3 $EXECUTABLE"
python3 $EXECUTABLE > $STDOUT 2> $STDERR


fi