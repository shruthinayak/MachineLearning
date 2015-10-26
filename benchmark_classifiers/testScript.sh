declare -a urls=('http://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wpbc.data' 'http://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data' 'http://archive.ics.uci.edu/ml/machine-learning-databases/ionosphere/ionosphere.data');
declare -a headers=('F' 'F' 'F');
declare -a classPosition=(2 2 35);

echo "\nEnter dataset between 1-3 or enter 0 to run all at once"
read choice

let choice=$choice-1

if [ $choice == -1 ]; then
	let start=0
	let end=2
elif [ $choice -ge 0 ] && [ $choice -le 3 ]; then
	let start=$choice
	let end=$choice
else
	echo "Wrong Choice"
	exit 1
fi


for (( i=$start; i<=$end; i++ ))
do
	echo 'Inputting url' ${urls[i]}
	Rscript benchmark.R ${urls[i]} ${headers[i]} ${classPosition[i]}	
done
