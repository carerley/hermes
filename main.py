from shop.sales import Sales

unavailable_black_totle = {
    'name': 'black tote',
    'url': 'https://www.hermes.com/us/en/product/herbag-zip-cabine-bag-H082835CKAC/'
}

available_hand_bag = {
    'name': 'white hand bag',
    'url': 'https://www.hermes.com/us/en/product/herbag-zip-cabine-bag-H077787CKAA/'
}

hand_bag2 = {
    'name': 'gold hand bag',
    'url': 'https://www.hermes.com/us/en/product/herbag-zip-cabine-bag-H077787CKAA/'
}

items_to_buy = [unavailable_black_totle, available_hand_bag, hand_bag2]

try:
    sales_person = Sales()
    sales_person.add_items(items_to_buy)
    sales_person.set_wait_time_second(3)
    sales_person.set_max_duration_hour(0.02)
    sales_person.run()
except RuntimeError as e:
    print(e)



