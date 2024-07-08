import sqlite3
from itertools import combinations

connection = sqlite3.connect('testing.db')

cursor = connection.cursor()

cursor.execute(""" 
SELECT * FROM purchase
""")

# Беру дані з бази даних.
raw_data = cursor.fetchall()

# Список всіх можливих значень.
list_of_items = ['headphones', 'keyboard', 'computer mouse', 'CPU', 'graphics card', 'RAM', 'SSD', 'hard drive disk', 'computer fan', 'controller']
number_of_product_purchases = {}

# st - це support. Це значення, від якого ми будемо відштовхуватися, щоб воно було менше за показник.
st = len(raw_data)/100 *40

#Для даних, які я відкидаю.
list_for_low_st = ['']

# Рахую загальну кількість разів, коли купували окремий продукт.
for x in raw_data:
    data = str(x[0]).split("|")
    for y in data:
        if y != '':
            if y not in number_of_product_purchases:
                number_of_product_purchases[y] = 1
            else:
                number_of_product_purchases[y] += 1

# Відкидаю всі дані, які не пройшли support.
for x in number_of_product_purchases:
    if number_of_product_purchases[x] < st:
        list_for_low_st.append(x)

# Список для всіх подвійних покупок.
buy_for_2_items = {}

# Для кожного списку в raw_data виділяю значення та поєдную їх між собою через ' and '.
for x in raw_data:
    data = str(x[0]).split("|")
    for i in range(len(data)):
        if data[i] not in list_for_low_st:
            for j in range(i + 1, len(data)):
                if data[j] not in list_for_low_st:
                    data_name = data[i] + ' and ' + data[j]
                    if data_name not in buy_for_2_items:
                        buy_for_2_items[data_name] = 1
                    else:
                        buy_for_2_items[data_name] += 1

# Відсортований та поєднаний список.
best_buy_for_2_items = {}

# Поєдную всі значення на основі правила A and B = B and A.
for item_pair, count in buy_for_2_items.items():
    items = item_pair.split(' and ')
    sorted_items = ' and '.join(sorted(items))
    
    if sorted_items in best_buy_for_2_items:
        best_buy_for_2_items[sorted_items] += count
    else:
        best_buy_for_2_items[sorted_items] = count

# Відкидаю всі подвійні покупки, які пройшли support.
best_buy_for_2_items_above_st = {}

# Відкидаю всі подвійні покупки, які не пройшли support.
for x in best_buy_for_2_items:
    if st < best_buy_for_2_items[x]: 
       best_buy_for_2_items_above_st[x] = best_buy_for_2_items[x]

#  Список для всіх можливих потрійних покупок.                  
combinations_of_3_count = {}

max_combination_size = 3

for item_tuple in raw_data:
    items = item_tuple[0].split('|')  # Розділияю рядок на список елементів.
    
    # Видаляю порожні рядки зі списку елементів.
    items = [item for item in items if item != '']
    
    for combination in combinations(items, 3):  # Створити комбінації розміром 3.
        sorted_combination = sorted(combination)
        key = ', '.join(sorted_combination)
        
        if key in combinations_of_3_count:
            combinations_of_3_count[key] += 1
        else:
            combinations_of_3_count[key] = 1

#  Список для всіх потрійних покупок.
best_buy_for_3_items = {}
# Проходжу кожен елементи у buy_for_3_items
for item_pair, count in combinations_of_3_count.items():
    items = item_pair.split(',')
    
    # Видаляю порожні рядки зі списку елементів.
    items = [item.strip() for item in items if item.strip() != '']
    
    # Створию всі можливі комбінації з 3 елементів.
    if len(items) >= 3:
        for combination in combinations(items, 3):
            sorted_combination = ', '.join(sorted(combination))
            
            if sorted_combination in best_buy_for_3_items:
                best_buy_for_3_items[sorted_combination] += count
            else:
                best_buy_for_3_items[sorted_combination] = count

#Список для всіх потрійних покупки, які пройшли support.
best_buy_for_3_items_above_st = {}

# Відкидаю всі потрійних покупок, які не пройшли support.
for x in best_buy_for_3_items:
    if st < best_buy_for_3_items[x]: 
       best_buy_for_3_items_above_st[x] = best_buy_for_3_items[x]

def calculate_association_metrics_fro_3(combinations, item_counts, raw_data, st, output_file , splits):
    for combo, count in combinations.items():
        items = combo.split(splits)  #Розділяю комбінацію, використовуючи кому як роздільник

        if len(items) != 3:
            continue  # Пропускаю недійсні комбінації. 

        item1, item2, item3 = items[0], items[1], items[2]

        # Розрахування підтримку (support) для кожного елементу.
        item1_support = number_of_product_purchases[item1] / len(raw_data)
        item2_support = number_of_product_purchases[item2] / len(raw_data)
        item3_support = number_of_product_purchases[item3] / len(raw_data)

        # Розрахувати достовірність (confidence) для трьохелементної комбінації.
        support = count / len(raw_data)

        # Розрахування достовірністі (confidence) для трьохелементної комбінації.
        confidence = support / (item1_support * item2_support)

        # Розрахування підтримки висоти (lift) для трьохелементної комбінації.
        lift = support / (item1_support * item2_support * item3_support)

        # Записати метрики у вихідний файл.
        output_file.write(f"{combo}: {count}\n")
        output_file.write(f"{item1} Support: {item1_support}\n")
        output_file.write(f"{item2} Support: {item2_support}\n")
        output_file.write(f"{item3} Support: {item3_support}\n")
        output_file.write(f"Support: {support}\n")
        output_file.write(f"Confidence: {confidence}\n")
        output_file.write(f"Lift: {lift}\n")
        output_file.write("\n")

def calculate_association_metrics(combinations, item_counts, raw_data, st, output_file , splits):
    
    frequent_combinations = {}
    
    for combo, count in combinations.items():
        items = combo.split(splits)  #Розділяю комбінацію, використовуючи кому як роздільник

        if len(items) != 2:
            continue # Пропускаю недійсні комбінації. 

        antecedent, consequent = items[0], items[1]

        # Розрахування підтримку (support) для кожного елементу.
        antecedent_support = item_counts[antecedent] / len(raw_data)
        consequent_support = item_counts[consequent] / len(raw_data)

        # Розрахування підтримки (support) для комбінації.
        support = count / len(raw_data)

        # Розрахування достовірністі (confidence) для трьохелементної комбінації.
        confidence = support / antecedent_support

        # Розрахування підтримки висоти (lift) для трьохелементної комбінації.
        lift = support / (antecedent_support * consequent_support)

        # Розрахувати leverage
        leverage = support - (antecedent_support * consequent_support)

        # Розрахувати conviction
        if confidence < 1:
            conviction = (1 - consequent_support) / (1 - confidence)
        else:
            conviction = float('inf')

        # Записати метрики у вихідний файл.
        output_file.write(f"{combo}: {count}\n")
        output_file.write(f"Antecedent Support: {antecedent_support}\n")
        output_file.write(f"Consequent Support: {consequent_support}\n")
        output_file.write(f"Support: {support}\n")
        output_file.write(f"Confidence: {confidence}\n")
        output_file.write(f"Lift: {lift}\n")
        output_file.write(f"Leverage: {leverage}\n")
        output_file.write(f"Conviction: {conviction}\n")
        output_file.write("\n")

with open('final_data.txt', 'w') as file:
    file.write("Frequent 2-item Combinations:\n")
    calculate_association_metrics(best_buy_for_2_items_above_st, number_of_product_purchases, raw_data, st, file, ' and ')
    
    file.write("Frequent 3-item Combinations:\n")
    calculate_association_metrics_fro_3(best_buy_for_3_items_above_st,number_of_product_purchases, raw_data, st, file, ', ')

    