import requests, bs4 , json
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/carros/batidos")
def batidosHome():
    urlDomain = 'http://373batidos.com.br'
    urlSite = 'http://373batidos.com.br/Veiculos.aspx'
    res = requests.get(urlSite)
    res.raise_for_status()
    data = {}
    data['site'] = urlDomain
    carsArray = []
    page = bs4.BeautifulSoup(res.text, "html.parser")
    veiculos = page.select('div #Veiculos-Anuncios')
    cars = page.find_all(attrs={"class": "Veiculo-Inner"})
    tempCar = {}  # dynamic var
    index = -1
    for tag in page.find_all(attrs={"class": "Veiculo-Inner"}):
        index += 1
        tempCar["car{0}".format(index)] = {}
        tempCar["car{0}".format(index)]['marca'] = tag.select('td.Veiculo-Info')[0].getText()
        tempCar["car{0}".format(index)]['modelo'] = tag.select('td.Veiculo-Info')[1].getText()
        tempCar["car{0}".format(index)]['ano'] = tag.select('td.Veiculo-RightInfo')[0].getText()

        funciona = tag.select('td.Veiculo-RightInfo')[1].getText();

        if (funciona.startswith('N')) : funciona='Nao'

        tempCar["car{0}".format(index)]['funciona'] = funciona
        tempCar["car{0}".format(index)]['preco'] = tag.find_next('b').getText()
        tempCar["car{0}".format(index)]['descricao'] = tag.select('#Img')[0]['alt']
        tempCar["car{0}".format(index)]['imagem'] = tag.select('#Img')[0]['src']

        carsArray.append(tempCar["car{0}".format(index)])

    data['found'] = len(cars)
    data['carros'] = carsArray
    print(str(int(len(cars))) + ' car(s) found')

    json_data = json.dumps(data)
    return json_data



if __name__ == '__main__':
    app.run(debug=True)
