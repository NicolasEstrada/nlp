#!/bin/bash
NIPS_HOME=/home/mestrada/devel/inf355/tarea1/nips
NIPS_LOGS=/home/mestrada/devel/inf355/tarea1/nips/logs

./vcluster $NIPS_HOME/nips00.mat -clmethod=direct -sim=cos -crfun=i1 -ntrials=10 -niter=10 -clabelfile=$NIPS_HOME/nips00.mat.clabel -rlabelfile=$NIPS_HOME/nips00.mat.rlabel -showfeatures 5 > $NIPS_LOGS/nips00.log
for i in {1..9}
	do
		./vcluster $NIPS_HOME/nips0$i.mat -clmethod=direct -sim=cos -crfun=i1 -ntrials=10 -niter=10 -clabelfile=$NIPS_HOME/nips0$i.mat.clabel -rlabelfile=$NIPS_HOME/nips0$i.mat.rlabel -showfeatures 5 > $NIPS_LOGS/nips0$i.log	
	done

for i in {10..12}
	do
		./vcluster $NIPS_HOME/nips$i.mat -clmethod=direct -sim=cos -crfun=i1 -ntrials=10 -niter=10 -clabelfile=$NIPS_HOME/nips$i.mat.clabel -rlabelfile=$NIPS_HOME/nips$i.mat.rlabel -showfeatures 5 > $NIPS_LOGS/nips$i.log
	done