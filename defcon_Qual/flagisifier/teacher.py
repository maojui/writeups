
#!/usr/bin/env bash
from keras.models import load_model, Model
from PIL import Image
import numpy as np

raw_model = load_model('./model.h5')
model = Model(input=raw_model.input, output=raw_model.layers[-2].output)

texts = ['RUNNEISOSTRICHESOWNINGMUSSEDPURIMSCIUI',
'MOLDERINGIINTELSDEDICINGCOYNESSDEFIECT',
'AMADOFIXESINSTIIIINGGREEDIIVDISIOCATIN',
'HAMIETSENSITIZINGNARRATIVERECAPTURINGU',
'EIECTROENCEPHAIOGRAMSPALATECONDOIESPEN',
'SCHWINNUFAMANAGEABLECORKSSEMICIRCIESSH',
'BENEDICTTURGIDITYDSYCHESPHANTASMAGORIA',
'TRUINGAIKALOIDSQUEILRETROFITBIEARIESTW',
'KINGFISHERCOMMONERSUERIFIESHORNETAUSTI',
'LIQUORHEMSTITCHESRESPITEACORNSGOALREDI',]

for file_index, text in zip(range(10), texts):
    images = []
    for i in range(1064//28):
        image = np.asarray(Image.open(f'images/sample_{file_index}.png')).reshape(1, 28, 1064, 1) 
        images.append(np.concatenate([image[:,:,28*i:28*(i+1)]]*38,2))

    images = np.concatenate(images)
    results = raw_model.predict(images)

    a = set()
    for result, c in zip(results, text):
        a.add( (np.argmax(result), c))
    