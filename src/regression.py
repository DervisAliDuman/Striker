import numpy as np
import matplotlib.pyplot as plt

FILE_NAME = "data.txt"

def read_data():
  with open(FILE_NAME, "r") as file:
      data = file.readlines()
      data = [i.replace("\n", "") for i in data]
      data = [i.split("\t") for i in data]
      for j in data:
        for i in range(len(j)):
          try:
            j[i] = float(j[i])
          except:
            continue
      return data

def append_data(data):
  with open(FILE_NAME, "a") as file:
    for i in data:
      file.write(f'{i[0]}\t{i[1]}\n')
    
# x'e bağlı y değeri tahmini
def calculatePredict():
  data_y = [i[1] for i in read_data()]
  data_x = [i[0] for i in read_data()]
  n = len(data_x)
  m_top = n * sum([data_x[i]*data_y[i] for i in range(n)]) - sum(data_x) * sum(data_y)
  m_bottom = n * sum([data_x[i]*2 for i in range(n)]) - (sum(data_x))*2
  m = m_top / m_bottom
  b = (sum(data_y) - m * sum(data_x)) / n
  return m, b
  # y = mx + b
  
def predict(goal_x):
  m, b = calculatePredict()
  return m * goal_x + b

# x topu atmadan önceki durum için kalenin merkezi ile görüntünün merkezi
# arasındaki yatay pixel mesafesi 640x480 bir görüntü için -300 ile 300 (-640/2 - 20, 640/2 + 20) değer aralığına sahip

# y değeri atıştan sonra topun gittiği noktanın merkeze olan yatay pixel mesafesi
# 640x480 bir görüntü için -300 ile 300 (-640/2 - 20, 640/2 + 20) değer aralığına sahip

# data.txt için
# sütun yapısı x y şeklindedir
#              0 1 
#              2 3
#              ...

def plot_scatter():
    datas = [i[1] for i in read_data()]
    # expression level değerlerini tutmak için liste oluşturduk
    totalBindingList = [i[0] for i in read_data()]
    # totalBindingList'e totalBinding fonksiyonundan dönen değeri atadık
    slope, constant = calculatePredict()
    # m, b ve predictions değerlerini slope, constant ve predictions değişkenlerine atadık
    x = np.linspace(int(min(totalBindingList)), int(max(totalBindingList)),100)
    # x değerlerini linspace fonksiyonu ile oluşturduk
    y = -slope * x - constant
    # y değerlerini oluşturduk
    plt.scatter(totalBindingList, datas)
    # scatter grafiğini çizdirdik
    plt.title(f'Red Line: y = {slope}*x + {constant}')
    # grafiğin başlığına m ve b değerlerini yazdırdık
    plt.plot(x, y, color = 'red')
    # hataları çizdirdik
    plt.legend(['Expression Levels', 'Linear Regression Line', 'Errors'])
    # grafiğin etiketlerini belirledik
    plt.xlabel('Total Binding Scores')
    # x ekseni için isim verdik
    plt.ylabel('Expression Levels')
    # y ekseni için isim verdik
    plt.show()
    # grafiği ekrana yazdırdık

