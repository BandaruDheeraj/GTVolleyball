from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask import request
from skimage import feature
import base64
from PIL import Image
from io import BytesIO
import numpy as np
import numpy as np
import requests
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import shift

app = Flask(__name__)
cors = CORS(app)


print('Loading Practice Data')
data = pd.read_excel('excel.xlsx', sheet_name=0)
print('Finished Loading')


print('Loading Game Data')
games = pd.read_excel('games.xlsx', sheet_name =0)
print('Finished Loading')


data = data.drop(columns = ['Unnamed: 8'])

practice_dates = data['date'].unique()
players = data['PLAYER NAME - CORRECTED'].unique()


print(games.keys())
new_games = games.set_index(['    Player Name', 'GAME_ID']).dropna()
print(new_games.index)

@app.route('/getPlayerData', methods = ['POST'])
def playerGetter():
    data1 = request.get_json()
    person = data1['person'].lower()
    y = person.split(' ')
    y[0] = y[0][0].upper() + y[0][1:]
    y[1] = y[1][0].upper() + y[1][1:]
    person = y[0] + " " + y[1]
    category = data1['category']
    
    fig, ax = plt.subplots(1, figsize = (18,5))
    
    new_games.loc[person][category].plot.bar(ax = ax, title = "Plot of %s's %s Data" % (person, category))
    ax.set_xlabel('Games by ID')
    ax.set_ylabel(category)
    ax.axhline(new_games.loc[person][category].mean(), linestyle = '--', color  = 'black')
    
    from io import BytesIO
    import base64

    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight',pad_inches=0)
    def convertback(buffer):
        img_str = base64.b64encode(buffer.getvalue())
        return img_str.decode('utf-8')

    returnval = convertback(buf)
    return jsonify("data:image/png;base64," + returnval)


@app.route('/getMatPlotLib', methods=['POST'])
def eyedetection():
    data1 = request.get_json()
    person = data1['person'].lower()
    if('gforce' in data1.keys()):
        force_val = float(data1['gforce'])
    else:
        force_val = 27.39012
        
    y = person.split(' ')
    y[0] = y[0][0].upper() + y[0][1:]
    y[1] = y[1][0].upper() + y[1][1:]
    person = y[0] + " " + y[1]
    practice = "  " + data1['practice']
    
    player = data.loc[np.bitwise_and(data['date'] == practice,
                        data['PLAYER NAME - CORRECTED'] == person)]
    
    i = np.array(player.index)
    
    player['diff'] = abs(player['gforce (G)'].shift(-1) - player['gforce (G)'])
    player.dropna()
    player['index_diff'] = i - shift(i, -1, cval=np.NaN)
    player = player[0:-1]
    player['stop'] = (player['index_diff'] <= -350)
    
    indeces = player[player['stop']].index
    
    fig = plt.figure(figsize = (18,5))
    plt.scatter(player.index, player['gforce (G)'])
    
    counter = 0
    for i in range(0, len(indeces)):
        partial = None
        if(i == 0):
            partial = player.loc[0:indeces[i]]
        elif(i == len(indeces) - 1):
            partial = player.loc[indeces[i]:]
        else:
            partial = player.loc[indeces[i]:indeces[i+1]]
        if(partial['gforce (G)'].max() > 27.39012432):
            plt.scatter(partial['gforce (G)'].idxmax(), partial['gforce (G)'].max(),  linewidths=100, marker = '+', color = 'green', s=500)
            counter+=1
        else:
            pass
        #print('Gforce avg for %d jump: %f' % (i+1, partial['gforce (G)'].mean()))
        #print('Max Gforce for %d jump: %f' % (i+1, partial['gforce (G)'].max()))
        #print('******************')
        plt.axvline(indeces[i], linestyle = '--', color = 'r')

    plt.axhline(player['gforce (G)'].mean(), linestyle = '--', color  = 'black')
    plt.axhline(force_val, color  = 'black')
    plt.xlabel('Index of Jump')
    plt.ylabel('GForce of Jump (G)')
    plt.title('Data of %s for practice %s' % (person, data1['practice']) )
    plt.legend()

    from io import BytesIO
    import base64

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight',pad_inches=0)
    def convertback(buffer):
        img_str = base64.b64encode(buffer.getvalue())
        return img_str.decode('utf-8')

    returnval = convertback(buf)
    return jsonify({"img": "data:image/png;base64," + returnval, "bad_counts": counter})

if __name__ == '__main__':
  app.run(host="0.0.0.0")
