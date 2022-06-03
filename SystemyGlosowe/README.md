# Systemy Głosowe
AGH lectures

### Wymagania:
- Pobranie próbek z: (https://www.kaggle.com/c/tensorflow-speech-recognition-challenge)<br />
**Note**: Potrzebne do odpalenia skryptów wszystkich części zadań 2 oraz 3

#### Zadanie 1
- Wykonanie kalkulatora głosowego z wykorzystaniem Speech-To-Text API Google (`Zad1_Audio_calculator.py`)

#### Zadanie 2
- **Part 1** (`Zad2_Speech_Recognition_CNN.ipynb`): <br />
Sprawdzono jakość klasyfikacji CNN wybranych pięciu słów z bazy nagrań w języku angielskim w zależności od liczebności zbioru treningowego.
- **Part 2** (`Zad2_Speech_Recognition_CNN_part2.ipynb`): <br />
Sprawdzenie metodologii z części 1 tego zadania dla wybranych pięciu słów (innych niż w części 1) poszerzonych o zbiór powstały w wyniku augumentacji (modyfikacji plików głosowych).

#### Zadanie 3
- **Part 1** (`Zad3_Speech_Classification_part1_kNN.ipynb` oraz `Zad3_Speech_Classification_part1_RFC_LR.ipynb`): <br />
Ocena oraz porównanie najlepszych wartości różnych zmiennych parametryzujących dla algorytmów k-najbliższych sąsiadów, losowego lasu oraz logistycznej regresji.
- **Part 2** (`Zad3_Speech_Classification_part2.ipynb`): <br />
Ocena algorytmów: Gaussian Naive Bayes, k-najbliższych sąsiadów oraz SVC pod względem różnych zmiennych parametryzujących oraz ich porównanie pod względem jakości działania dla różnej wielkości zbiorów treningowych i testowych.

#### Pozostałe 
- Folder `Zad3_database` zawiera metadane w celu możliwości wykonania się skryptów z zadania 3.
- Pozostałe pliki .ipynb są skryptami pomocniczymi, edukacyjnymi (mało istotne). 
