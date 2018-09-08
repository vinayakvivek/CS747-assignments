DIR=150050098
mkdir $DIR
cp -r extras $DIR
cp encodeGambler.sh $DIR
cp planner.sh $DIR
cp 150050098_report.pdf $DIR

tar -cvzf 150050098.tar.gz 150050098/
rm -rf 150050098