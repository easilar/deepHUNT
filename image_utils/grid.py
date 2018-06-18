#Dictinary for grid

Grid = {
'optimisers':{

'SGD':{
'lrs':[0.001, 0.01, 0.1, 0.2 , 0.3],
'momentums': [0.01, 0.2, 0.4 ,0.6, 0.8 ,0.9]
},
'Adadelta':{ 
'lrs': [0.01, 0.01, 0.1, 0.5, 0.8 ,1.0],
'momentums': [0.01, 0.2, 0.6, 0.9, 0.95] 
},
'Adam':{
'lrs': [0.001, 0.002 , 0.1 , 0.3 , 0.5 , 0.9],
'momentums': [0.9]
},
'Nadam':{
'lrs': [0.001, 0.002, 0.003, 0.01, 0.5],
'momentums': [0.9]
}

}





}

