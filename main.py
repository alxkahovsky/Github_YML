# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import csv
import pymongo

# Запустили сервер Mongo DB на локалке
client = pymongo.MongoClient('localhost', 27017)
db = client['Groups_id']
series_collection = db['Groups']
# Очистили БД
series_collection.delete_many({})
# Функция поиска по БД
def find_document(collection, elements, multiple=True):
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)

def fileFinder(filename):
    result = find_document(series_collection, {'Core_group': filename})
    try:
        return(result)
    except:
        print('Not  found!')
# Читаем построчно CSV таблицу, считываем 4 и 5 ячейки с именами групп товаров и их id
with open('table example.csv', 'r') as f:
    reader = csv.reader(f, delimiter=";")
    i = 0
    group_pool = []
    for row in reader:
        grouplist = row[3]
        idlist = row[4]
        grouplist = grouplist.split(',')
        idlist = idlist.split(',')
        for num in range(len(idlist)):
            if num == 0 and not grouplist[num] in group_pool:
                group_pool.append(grouplist[num])
                series_collection.insert_one(
                    {'Core_gr': grouplist[num], 'id': idlist[num]}) # создаем записи в БД для категорий
            elif not grouplist[num] in group_pool:
                group_pool.append(grouplist[num])
                series_collection.insert_one(
                    {'Sub_gr': grouplist[num], 'id': idlist[num], 'Parent_id': idlist[num-1], 'Parent_gr': grouplist[num-1]  }) # создаем записи для подкатегорий с указанием родительского id

def findALL():
    result = find_document(series_collection, {})
    try:
        return(result)
    except:
        print('Not  found!')

test = findALL()  # записываем результат функции в переменную

env = Environment(
    loader=FileSystemLoader('C:\\Users\\Пользователь\\PycharmProjects\\YMLscript\\'),
    trim_blocks=True,
    lstrip_blocks=True)
template = env.get_template('YML_sample(2).xml')

with open('table example.csv', 'r') as f:
    reader = csv.reader(f, delimiter=";")
    urls = []
    price = []
    ids = []
    imgs = []
    names = []
    cat_ids = []
    for row in reader:
        urls.append('https://shop-url.ru' + row[0])# в таблице указан путь без домена
        price.append(row[5])
        ids.append(row[1])
        imgs.append('https://shop-url.ru/media/' + row[6])# # в таблице указан путь без домена
        names.append(row[2])
        category_id = row[4]
        category_id = category_id.split(',')
        cat_ids.append(category_id[-1])

offers = []
for u, p, i, im, n, cat in zip(urls, price, ids, imgs, names, cat_ids):
    offer = []
    offer.append(u)
    offer.append(p)
    offer.append(i)
    offer.append(im)
    offer.append(n)
    offer.append(cat)
    offers.append(offer)

data = {
    'test': test,
    'offers': offers,
}
with open('Яндекс_фид' + '.xml', "w", encoding = 'utf-8') as file:
    print(template.render(data), file=file)

print("YML фид сформирован")
# Очистили БД
series_collection.delete_many({})




