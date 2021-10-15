# importação das bibliotecas utilizadas
import pandas as pd
from difflib import SequenceMatcher


# carregando os filmes indicados ou vencedores do Oscar em um dataframe
# e examinando as características do dataframe
oscar_movies = pd.read_csv('kaggle/input/the-oscar-award/the_oscar_award.csv')
oscar_movies.info()
oscar_movies.describe()



# A única coluna com itens faltantes é a coluna film.
# Vamos explorar as linhas em que faltam esses dados para entender o porquê,
# e em quais categorias isso está ocorrendo
print(oscar_movies[oscar_movies['film'].isnull()]['category'].unique())
oscar_movies[oscar_movies['film'].isnull()].head()


# Alguns desses casos se tratam de prêmios honorários, humanitários e memoriais -
# ou seja, não relacionados a filmes específicos. Podemos desconsiderar essas linhas
rows_to_drop = oscar_movies[
    (oscar_movies['category'] == 'HONORARY AWARD') |
    (oscar_movies['category'] == 'SPECIAL AWARD') |
    (oscar_movies['category'] == 'IRVING G. THALBERG MEMORIAL AWARD') |
    (oscar_movies['category'] == 'JEAN HERSHOLT HUMANITARIAN AWARD') |
    (oscar_movies['category'] == 'SPECIAL ACHIEVEMENT AWARD')
].index

oscar_movies = oscar_movies.drop(rows_to_drop)

print(oscar_movies[oscar_movies['film'].isnull()]['category'].unique())
oscar_movies[oscar_movies['film'].isnull()].head()



# As linhas restantes com dados faltantes na coluna filme são de categorias
# que precisam necessariamente estar ligadas a um filme.

# Para duas dessas categorias, ligadas a filmes estrangeiros, o nome do filme parece constar
# na coluna 'name'

for row in oscar_movies[
    (oscar_movies['category'] == 'SPECIAL FOREIGN LANGUAGE FILM AWARD') |
    (oscar_movies['category'] == 'HONORARY FOREIGN LANGUAGE FILM AWARD')
].iterrows():
    print(row[1][4])

# em todos esses casos, com exceção do último, o nome do filme consta na coluna 'name',
# seguido de hífen. Podemos aplicar a mesma regra para todos os casos, e transpor o nome do
# filme para a coluna film
oscar_movies['film'] = oscar_movies.apply(
    lambda x: x['name'].split('-')[0] if x['category'] in (
        'SPECIAL FOREIGN LANGUAGE FILM AWARD', 'HONORARY FOREIGN LANGUAGE FILM AWARD'
    )
    else x['film'],
    axis=1
)

# Com os dados dessas categorias corrigidos,
# é hora de checar os dados que ainda são faltantes
print(oscar_movies[oscar_movies['film'].isnull()]['category'].unique())
oscar_movies[oscar_movies['film'].isnull()].head()


# Outras linhas com dados faltantes na coluna 'film' são de obtenção difícil ou imprecisa:
# um assistente de direção, por exemplo, pode ter tido mais de um filme lançado num mesmo
# ano, o que faria a checagem dos dados restantes muito trabalhosa.
# Essas colunas serão ignoradas.
rows_to_drop = oscar_movies[
    (
        (oscar_movies['category'] == 'ENGINEERING EFFECTS') |
        (oscar_movies['category'] == 'WRITING (Title Writing)') |
        (oscar_movies['category'] == 'SOUND RECORDING') |
        (oscar_movies['category'] == 'ASSISTANT DIRECTOR')
    ) & (oscar_movies['film'].isnull())
].index

oscar_movies = oscar_movies.drop(rows_to_drop)

oscar_movies.info()




# Um fato que pode ser observado analisando esses dados restantes é que algumas das
# categorias tiveram mudanças de nomes - como foi o caso na premiação de filme de língua
# estrangeira. Já outras categorias desapareceram da premiação ("melhor filme em preto e
# branco") ou foram incluídas.

# A categoria mais recente incluída na premiação é a de melhor filme de animação, criada em
# 2002. Por isso, iremos desconsiderar filmes anteriores a essa data.

rows_to_drop = oscar_movies[(oscar_movies['year_ceremony'] < 2002)].index
oscar_movies = oscar_movies.drop(rows_to_drop)

# Iremos desconsiderar ainda a premiação de edição de som (sound editing),
# que foi descontinuada em 2019, a única removida após o ano de 2002.
rows_to_drop = oscar_movies[(oscar_movies['category'] == 'SOUND EDITING')].index
oscar_movies = oscar_movies.drop(rows_to_drop)

list(oscar_movies['category'].unique())


# Algumas dessas categorias também precisaram de consolidação, já que seus nomes
# aparecem de formas diferentes. Foram utilizados os nomes mais recentes.

category_renaming = {
    'FOREIGN LANGUAGE FILM': 'INTERNATIONAL FEATURE FILM',
    'ART DIRECTION': 'PRODUCTION DESIGN',
    'WRITING (Screenplay Based on Material Previously Produced or Published)': 'WRITING (Adapted Screenplay)',
    'WRITING (Screenplay Written Directly for the Screen)': 'WRITING (Original Screenplay)',
    'SOUND MIXING': 'SOUND',
    'MAKEUP': 'MAKEUP AND HAIRSTYLING',
}

oscar_movies['category'] = oscar_movies.apply(
    lambda x: category_renaming[x['category']]
    if x['category'] in category_renaming
    else x['category'],
    axis=1
)

# Checando que agora temos as 23 categorias atuais do Oscar
list(oscar_movies['category'].unique())


# Agora precisamos unir os dados do dataset do Oscar ao dataset de metadados de filmes.

# carregando os metadados de todos os filmes
movies_metadata = pd.read_csv(
    'kaggle/input/the-movies-dataset/movies_metadata.csv',
)

# converter coluna release_date para datetime
movies_metadata['release_date'] = movies_metadata['release_date'].apply(
    lambda x: pd.to_datetime(x, errors='coerce'),
)

# examinando as características do dataframe
movies_metadata.info()
movies_metadata.describe()
movies_metadata.head()


# Adicionando uma coluna com o ano de lançamento do filme, que será útil em outras análises
movies_metadata['release_year'] = movies_metadata['release_date'].apply(
    lambda x: x.year
)


# Precisamos retirar os filmes pós 2017 do dataset do oscar, já que não estão presentes no The Movie Dataset
rows_to_drop = oscar_movies[(oscar_movies['year_film'] > 2017)].index
oscar_movies = oscar_movies.drop(rows_to_drop)

oscar_movies['year_film'].describe()



# Normalização de nomes para comparação entre os dois datasets
def normalize(name):
    normalized_name = name
    try:
        for character in [
            ':', '!', '?', ' -', '- ', '-', '... ', '...', '/', "'", '.', '·', ',', '"'
        ]:
            normalized_name = normalized_name.replace(character, '')

        for foreign_character, replacement in {
            'ž': 'z',
            'ń': 'n',
        }.items():
            normalized_name = normalized_name.replace(foreign_character, replacement)

        normalized_name = normalized_name.lower()

    except:
        pass

    return normalized_name


movies_metadata['title'] = movies_metadata['title'].apply(normalize)
movies_metadata['original_title'] = movies_metadata['original_title'].apply(normalize)
oscar_movies['film'] = oscar_movies['film'].apply(normalize)



metadata_english_titles = {
    movie[1]['title']: movie[1]['release_year']
    for movie in movies_metadata.iterrows()
}

metadata_original_titles = {
    movie[1]['original_title']: (movie[1]['release_year'], movie[1]['title'])
    for movie in movies_metadata.iterrows()
}



# checar filmes do Oscar que não estão no dataset de metadados
not_in_metadata_database = {}
in_metadata_database = {}

oscar_titles = {
    movie[1]['film']: movie[1]['year_film']
    for movie in oscar_movies.iterrows()
}

# Considerar títulos originais e em inglês no dataset do Oscar
for complete_title, year in oscar_titles.items():
    found = False

    if complete_title in metadata_english_titles and metadata_english_titles[complete_title] == year:
        in_metadata_database[complete_title] = year
        found = True

    elif complete_title in metadata_original_titles and metadata_original_titles[complete_title][0] == year:
        english_title = metadata_original_titles[complete_title][1]
        oscar_movies.loc[
            (oscar_movies['film'] == complete_title) & (oscar_movies['year_film'] == year)
            ]['film'] = english_title
        in_metadata_database[english_title] = year
        found = True

    if not found:
        # Se não encontrado, considerar caso especial: filmes com os dois títulos no nome, separados por parênteses
        titles = [
            title for title in
            complete_title.replace('(', '*****').replace(')', '*****').split('*****')
            if title
        ]
        for title in titles:
            if title in metadata_english_titles and metadata_english_titles[title] == year:
                in_metadata_database[title] = year
                found = True
                break

            elif title in metadata_original_titles and metadata_original_titles[title][0] == year:
                english_title = metadata_original_titles[title][1]
                oscar_movies.loc[
                    (oscar_movies['film'] == title) & (oscar_movies['year_film'] == year)
                ]['film'] = english_title
                in_metadata_database[english_title] = year
                found = True
                break

    # se ainda não encontrado, adicionar à lista de filmes não encontrados
    if not found:
        not_in_metadata_database[complete_title] = year


print(len(in_metadata_database), 'found')
print(len(not_in_metadata_database), 'not found')


# Checar filmes que podem estar com nomes levemente diferentes nas duas plataformas,
# realizando uma análise de similaridade entre os títulos normalizados

def similarity(a, b):
    try:
        return SequenceMatcher(None, a, b).ratio()
    except:
        return 0


i = 0
total = len(not_in_metadata_database)
possibly_found = {}

for title, year in not_in_metadata_database.items():
    i += 1
    print(f'Movie {i} of {total}')
    best_match = 0

    for other_title, other_year in metadata_english_titles.items():
        title_similarity = similarity(title, other_title)

        if year == other_year and title_similarity > best_match:
            best_match = title_similarity
            possibly_found[title] = other_title, year, title_similarity

possibly_found_formatted = sorted(
    [
        (title_oscar, title_metadata, year, title_similarity)
        for title_oscar, (title_metadata, year, title_similarity)
        in possibly_found.items()
    ],
    key=lambda x: x[3]
)

print('Not found movies:', possibly_found_formatted, end='\n\n')



# with open('possibly_found', 'w') as file:
#     file.write(str(possibly_found_formatted))




# Filmes que podem ser reconhecidos nas duas listas:
movies_to_rename = {
    'harry potter and the sorcerers stone': 'harry potter and the philosophers stone',
    'wallace & gromit in the curse of the wererabbit': 'the curse of the wererabbit',
    'mt head': 'mount head',
    'wardance': 'war dance',
}