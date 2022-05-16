from shop.sales import Sales

unavailable_black_totle = {
    'name': 'black tote',
    'url': 'https://www.hermes.com/us/en/product/herbag-zip-cabine-bag-H082835CKAC/'
}

available_hand_bag = {
    'name': 'white hand bag',
    'url': 'https://www.hermes.com/us/en/product/herbag-zip-cabine-bag-H077787CKAA/'
}

items_to_buy = [available_hand_bag]


try:
    sales_person = Sales()
    sales_person.add_items(items_to_buy)
    sales_person.run()
except RuntimeError as e:
    print(e)



