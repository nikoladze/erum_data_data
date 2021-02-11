### This is a template file meant to be a guideline to smooth out the implementation of our models in the same framework. 
##	William Korcari: william.korcari@desy.de 	

import erum_data_data as edd
import tensorflow as tf

##	Please add the model generating function and the preprocessing function in that file.
from particle_net import Network as topNet
##	utils.py is the file that contains all the self-built methods of this script.
from utils import train_plots
from utils import roc_auc
from utils import test_accuracy
from utils import test_f1_score


#########################################
#####  EXAMPLE IMPLEMENTATION OF FCN  ###

#nn = Network()
nn = topNet()
datasets =  nn.compatible_datasets

for ds in datasets:  

	X_train, y_train  = ds.load(split='train')
	X_test, y_test = ds.load(split='test')

	#max_e = 100000#<-- this trains already well#1000#-1#100000
	#max_t = 10000#-1#100000
	#X_train[0] = X_train[0][0:max_e]
	#X_test[0] = X_test[0][0:max_t]
	#y_train = y_train[0:max_e]
	#y_test = y_test[0:max_t]
	x_train = nn.preprocessing(X_train[0])
	x_test  = nn.preprocessing(X_test[0])
	
	model = nn.model_lite(nn.get_shapes(x_train))
	model.compile(**nn.compile_args)
	history = model.fit(x = x_train, y = y_train, **nn.fit_args)

	##	From here on, one should be able to use already defined methods as showed in the following lines. 
	##	Let us know if you face any issues with that.

	#training history plots
	label = "plot"
	train_plots(history, label, True)

	#evaluation plots and scores
	y_pred = model.predict(x_test).ravel()
	roc_auc(y_pred, y_test, label, True)
	test_accuracy(y_pred, y_test, label)
	test_f1_score(y_pred, y_test, label)


