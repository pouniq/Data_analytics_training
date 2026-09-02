"""
Kohannegar Synthetic Dataset Generator
Generates realistic, schema-compliant synthetic MySQL data based on specification_business.txt.
Output: data_output.sql
"""

import random
import string
from datetime import datetime, timedelta

def main():
    print("Starting Kohannegar Synthetic Dataset Generation...")
    
    # Seed for reproducibility
    random.seed(42)

    # -------------------------------------------------------------------------
    # 1. CATEGORIES (~30 rows)
    # -------------------------------------------------------------------------
    top_categories = [
        (1, "Poetry Books"),
        (2, "Historical Books"),
        (3, "Paintings"),
        (4, "Photography Books"),
        (5, "Artist Collection Books"),
        (6, "Rare Manuscripts")
    ]

    sub_categories_data = [
        # Poetry Books (Parent 1)
        (1, "Classical Persian Poetry", 9),
        (1, "Contemporary Poetry", 5),
        (1, "Translated World Poetry", 5),
        (1, "Illustrated Poetry Editions", 8),
        # Historical Books (Parent 2)
        (2, "Ancient Persia", 7),
        (2, "Islamic Era History", 6),
        (2, "Modern Iranian History", 5),
        (2, "World History", 5),
        (2, "Local/Regional History", 5),
        # Paintings (Parent 3)
        (3, "Miniature Reproductions", 5),
        (3, "Oil Painting Books", 5),
        (3, "Watercolor Collections", 5),
        (3, "Calligraphy Art", 5),
        # Photography Books (Parent 4)
        (4, "Black & White Photography", 6),
        (4, "Landscape Photography", 7),
        (4, "Portrait Photography", 5),
        (4, "Documentary Photography", 5),
        # Artist Collection Books (Parent 5)
        (5, "Single-Artist Retrospectives", 8),
        (5, "Limited Edition Artist Sets", 5),
        (5, "Signed Artist Collections", 5),
        # Rare Manuscripts (Parent 6)
        (6, "Antique Reprints", 5),
        (6, "Facsimile Editions", 5),
        (6, "Numbered Collector Editions", 4)
    ]

    categories = []
    for cat_id, title in top_categories:
        categories.append({
            "id": cat_id,
            "title": title,
            "parent_id": None,
            "weight": 5
        })

    cat_counter = 7
    sub_cat_list = []
    for parent_id, title, base_weight in sub_categories_data:
        jitter = random.choice([-1, 0, 1]) if base_weight == 5 else 0
        final_weight = max(1, min(10, base_weight + jitter))
        cat_obj = {
            "id": cat_counter,
            "title": title,
            "parent_id": parent_id,
            "weight": final_weight
        }
        categories.append(cat_obj)
        sub_cat_list.append(cat_obj)
        cat_counter += 1

    for parent_cat in categories:
        if parent_cat["parent_id"] is None:
            subs = [c["weight"] for c in sub_cat_list if c["parent_id"] == parent_cat["id"]]
            if subs:
                parent_cat["weight"] = sum(subs) / len(subs)

    print(f"Generated {len(categories)} categories.")

    # -------------------------------------------------------------------------
    # 2. PRODUCTS (~200 rows)
    # -------------------------------------------------------------------------
    price_ranges = {
        1: (1_000_000, 15_000_000),
        2: (2_000_000, 30_000_000),
        3: (5_000_000, 120_000_000),
        4: (3_000_000, 40_000_000),
        5: (10_000_000, 180_000_000),
        6: (20_000_000, 250_000_000)
    }

    adjectives = ["Golden", "Ancient", "Eternal", "Coastal", "Royal", "Mystic", "Imperial", "Silent", "Celestial", "Sacred", "Vintage", "Classic"]
    nouns = ["Verses", "Chronicles", "Reflections", "Masters", "Echoes", "Heritage", "Visions", "Treasures", "Symphony", "Whispers", "Memoirs", "Legacy"]
    
    products = []
    prod_id = 1
    total_sub_weight = sum(c["weight"] for c in sub_cat_list)
    
    for sub in sub_cat_list:
        p_count = int(round((sub["weight"] / total_sub_weight) * 200))
        p_count = max(5, min(12, p_count))
        
        parent_id = sub["parent_id"]
        min_p, max_p = price_ranges[parent_id]
        
        for _ in range(p_count):
            adj = random.choice(adjectives)
            noun = random.choice(nouns)
            title = f"{adj} {sub['title'].split()[0]} {noun} Vol. {random.randint(1, 99)}"
            while any(p["title"] == title for p in products):
                title = f"{adj} {sub['title'].split()[0]} {noun} #{random.randint(100, 999)}"
                
            raw_price = random.randint(min_p, max_p)
            rounded_price = int(round(raw_price / 10000.0) * 10000)
            detail = f"A fine collection of {sub['title'].lower()} curated for art and literature connoisseurs. Features high quality printing and detailed annotations."
            
            products.append({
                "id": prod_id,
                "title": title,
                "detail": detail,
                "price": rounded_price,
                "category_id": sub["id"],
                "parent_category_id": parent_id,
                "sub_title": sub["title"],
                "sales_tier": None
            })
            prod_id += 1

    high_pop_subs = ["Classical Persian Poetry", "Single-Artist Retrospectives", "Landscape Photography"]
    low_pop_subs = ["Numbered Collector Editions", "Limited Edition Artist Sets"]

    high_prod_indices = [i for i, p in enumerate(products) if p["sub_title"] in high_pop_subs]
    low_prod_indices = [i for i, p in enumerate(products) if p["sub_title"] in low_pop_subs]
    remaining_indices = [i for i in range(len(products)) if i not in high_prod_indices and i not in low_prod_indices]

    num_bestsellers = int(len(products) * 0.10)
    num_lowsellers = int(len(products) * 0.35)

    random.shuffle(high_prod_indices)
    random.shuffle(low_prod_indices)
    random.shuffle(remaining_indices)

    bestseller_indices = set(high_prod_indices[:num_bestsellers])
    if len(bestseller_indices) < num_bestsellers:
        needed = num_bestsellers - len(bestseller_indices)
        bestseller_indices.update(remaining_indices[:needed])
        remaining_indices = remaining_indices[needed:]

    lowseller_indices = set(low_prod_indices[:num_lowsellers])
    if len(lowseller_indices) < num_lowsellers:
        needed = num_lowsellers - len(lowseller_indices)
        lowseller_indices.update(remaining_indices[:needed])
        remaining_indices = remaining_indices[needed:]

    for i, p in enumerate(products):
        if i in bestseller_indices:
            p["sales_tier"] = "bestseller"
        elif i in lowseller_indices:
            p["sales_tier"] = "low_seller"
        else:
            p["sales_tier"] = "mid_seller"

    print(f"Generated {len(products)} products.")

    # -------------------------------------------------------------------------
    # 3. USERS (~1500 rows)
    # -------------------------------------------------------------------------
    first_names = [
        "Ali", "Mohammad", "Reza", "Amir", "Hossein", "Mehdi", "Saeed", "Hamid", "Farhad", "Kaveh",
        "Arash", "Babak", "Daryoush", "Shorah", "Ehsan", "Pouriya", "Saman", "Arman", "Navid", "Ramin",
        "Sara", "Maryam", "Narges", "Zahra", "Fatemeh", "Elnaz", "Niloufar", "Pariyan", "Shirin", "Aida",
        "Mina", "Roxana", "Mahsa", "Sahar", "Sanaz", "Sepideh", "Taras", "Yasaman", "Bahar", "Pegah",
        "Hamidreza", "Alireza", "Ahmad", "Mahmoud", "Sina", "Nima", "Sohrab", "Kamran", "Keyvan", "Behnam",
        "Ladan", "Kobra", "Somayeh", "Khatereh", "Hoda", "Arezoo", "Parisa", "Ghazal", "Atousa", "Monir"
    ]
    
    last_names = [
        "Rezaei", "Mohammadi", "Ahmadi", "Hosseini", "Karimi", "Ghasemi", "Ghorbani", "Ebrahimi", "Rahimi", "Jafari",
        "Mousavi", "Abbasi", "Taheri", "Bagheri", "Sharifi", "Salehi", "Hashemi", "Moradi", "Pirouz", "Abedi",
        "Mirzai", "Kazemi", "Rostami", "Nouri", "Khani", "Sadeghi", "Sultani", "Najafi", "Shahidi", "Fathi",
        "Ranjbar", "Poursaeed", "Mahdavi", "Soleimani", "Tavasoli", "Habibi", "Farhadi", "Azizi", "Khosravi", "Danesh",
        "Moghadam", "Kiani", "Zand", "Afshar", "Tehrani", "Shirazi", "Rashti", "Anzali", "Ghanbari", "Eshghi",
        "Ramsari", "Gilani", "Javadi", "Vafaei", "Zarei", "Gholami", "Pasha", "Sardari", "Kashani", "Nasseri"
    ]

    users = []
    usernames_seen = set()
    start_reg = datetime(2021, 1, 1)
    end_reg = datetime(2026, 8, 1)
    cutoff_12m = datetime(2025, 8, 1)

    for i in range(1, 1501):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        
        base_uname = f"{fn.lower()}.{ln.lower()}".replace(" ", "")
        uname = base_uname
        if uname in usernames_seen:
            uname = f"{base_uname}{random.randint(10, 99)}"
        while uname in usernames_seen:
            uname = f"{base_uname}{random.randint(100, 999)}"
        usernames_seen.add(uname)

        pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        age_r = random.random()
        if age_r < 0.15:
            age = random.randint(18, 29)
        elif age_r < 0.55:
            age = random.randint(30, 39)
        elif age_r < 0.90:
            age = random.randint(40, 50)
        else:
            age = random.randint(51, 65)

        birth_year = 2026 - age
        birth_date = datetime(birth_year, random.randint(1, 12), random.randint(1, 28)).strftime("%Y-%m-%d")

        city_r = random.random()
        if city_r < 0.55:
            city = "Rasht"
        elif city_r < 0.80:
            city = "Nowshahr"
        else:
            city = "Bandar Anzali"

        is_recent = random.random() < 0.40
        if is_recent:
            days_diff = (end_reg - cutoff_12m).days
            reg_dt = cutoff_12m + timedelta(days=random.randint(0, days_diff))
        else:
            days_diff = (cutoff_12m - start_reg).days
            reg_dt = start_reg + timedelta(days=random.randint(0, days_diff))

        if random.random() < 0.25 and reg_dt.month not in [9, 10, 11, 12]:
            new_month = random.choice([9, 10, 11, 12])
            try:
                reg_dt = reg_dt.replace(month=new_month)
            except ValueError:
                reg_dt = reg_dt.replace(month=new_month, day=28)

        register_date = reg_dt.strftime("%Y-%m-%d %H:%M:%S")
        disabled = 1 if random.random() < 0.12 else 0
        is_repeat = random.random() < 0.35

        users.append({
            "id": i,
            "first_name": fn,
            "last_name": ln,
            "user_name": uname,
            "password": pwd,
            "birth_date": birth_date,
            "city": city,
            "register_date": register_date,
            "reg_datetime": reg_dt,
            "disabled": disabled,
            "is_repeat": is_repeat
        })

    print(f"Generated {len(users)} users.")

    # -------------------------------------------------------------------------
    # 4. ROLES & 5. ROLES_USER
    # -------------------------------------------------------------------------
    roles = [(1, "admin"), (2, "staff"), (3, "customer")]
    roles_user = []
    for u in users:
        roles_user.append((3, u["id"]))

    staff_users = random.sample(users, random.randint(8, 12))
    for u in staff_users:
        roles_user.append((2, u["id"]))

    admin_users = random.sample(users, random.randint(2, 3))
    for u in admin_users:
        roles_user.append((1, u["id"]))

    print(f"Generated roles and {len(roles_user)} roles_user mappings.")

    # -------------------------------------------------------------------------
    # 9. DISCOUNT (~30 rows)
    # -------------------------------------------------------------------------
    discounts = []
    disc_id = 1
    months_names = {2: "February", 4: "April", 6: "June", 8: "August", 10: "October", 12: "December"}
    
    for year in [2025, 2026]:
        for m in [2, 4, 6, 8, 10, 12]:
            if year == 2026 and m > 8:
                continue
            last_day = 29 if (m == 2 and year % 4 == 0) else (28 if m == 2 else (30 if m in [4, 6, 9, 11] else 31))
            code = f"BIMONTH{year}{m:02d}"
            discounts.append({
                "id": disc_id,
                "title": f"End of {months_names[m]} 15% Storewide Discount",
                "discount_code": code,
                "percentage": 15,
                "active_date": f"{year}-{m:02d}-25",
                "expire_date": f"{year}-{m:02d}-{last_day}",
                "is_bimonthly": True
            })
            disc_id += 1

    extra_discounts = [
        ("Yalda Night Poetry Special", 15, "2025-12-15", "2025-12-21"),
        ("Nowruz New Year Gift Discount", 15, "2025-03-15", "2025-04-03"),
        ("Nowruz New Year Gift Discount", 15, "2026-03-15", "2026-04-03"),
        ("New Customer Welcome Discount", 10, "2021-01-01", "2026-12-31"),
        ("Rare Manuscript Collector Days", 10, "2025-05-10", "2025-05-14"),
        ("Rare Manuscript Collector Days", 10, "2025-11-10", "2025-11-14"),
        ("Rare Manuscript Collector Days", 10, "2026-05-10", "2026-05-14"),
        ("Photography Book Summer Sale", 15, "2025-06-01", "2025-08-31"),
        ("Photography Book Summer Sale", 15, "2026-06-01", "2026-08-31"),
    ]

    for title, pct, act, exp in extra_discounts:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        discounts.append({
            "id": disc_id,
            "title": title,
            "discount_code": code,
            "percentage": pct,
            "active_date": act,
            "expire_date": exp,
            "is_bimonthly": False
        })
        disc_id += 1

    while len(discounts) < 30:
        year = random.choice([2025, 2026])
        month = random.randint(1, 8 if year == 2026 else 12)
        day = random.randint(1, 20)
        act_dt = datetime(year, month, day)
        exp_dt = act_dt + timedelta(days=random.randint(3, 7))
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        pct = random.choice([5, 10, 15, 20])
        discounts.append({
            "id": disc_id,
            "title": f"Flash Special Sale {disc_id}",
            "discount_code": code,
            "percentage": pct,
            "active_date": act_dt.strftime("%Y-%m-%d"),
            "expire_date": exp_dt.strftime("%Y-%m-%d"),
            "is_bimonthly": False
        })
        disc_id += 1

    print(f"Generated {len(discounts)} discounts.")

    # -------------------------------------------------------------------------
    # 6. ORDERS (~7000 rows)
    # -------------------------------------------------------------------------
    orders = []
    order_id = 1
    month_weights = {1: 0.9, 2: 1.3, 3: 0.8, 4: 1.0, 5: 0.9, 6: 1.3, 7: 0.8, 8: 0.9, 9: 1.1, 10: 1.0, 11: 1.2, 12: 1.6}

    for u in users:
        if u["is_repeat"]:
            num_o = random.randint(3, 15)
        else:
            num_o = random.choices([0, 1, 2], weights=[0.4, 0.4, 0.2])[0]

        for _ in range(num_o):
            min_dt = u["reg_datetime"]
            max_dt = datetime(2026, 8, 31)
            
            if min_dt >= max_dt:
                min_dt = max_dt - timedelta(days=30)

            possible_months = []
            curr = min_dt
            while curr <= max_dt:
                possible_months.append((curr.year, curr.month))
                if curr.month == 12:
                    curr = datetime(curr.year + 1, 1, 1)
                else:
                    curr = datetime(curr.year, curr.month + 1, 1)

            if not possible_months:
                possible_months = [(2026, 8)]

            m_weights = [month_weights[m[1]] for m in possible_months]
            chosen_year, chosen_month = random.choices(possible_months, weights=m_weights)[0]
            last_day = 28 if chosen_month == 2 else (30 if chosen_month in [4, 6, 9, 11] else 31)
            
            if chosen_month in [2, 4, 6, 8, 10, 12] and random.random() < 0.45:
                day = random.randint(max(1, last_day - 3), last_day)
            else:
                day = random.randint(1, last_day)

            order_dt = datetime(chosen_year, chosen_month, day, random.randint(8, 21), random.randint(0, 59))
            if order_dt < u["reg_datetime"]:
                order_dt = u["reg_datetime"] + timedelta(hours=random.randint(1, 48))

            if order_dt.weekday() not in [3, 4] and random.random() < 0.25:
                days_to_add = (3 - order_dt.weekday()) % 7
                order_dt = order_dt + timedelta(days=days_to_add)

            sales_channel = "online" if random.random() < 0.65 else "in_person"
            was_paid = 1 if random.random() < 0.92 else 0

            orders.append({
                "id": order_id,
                "user_id": u["id"],
                "order_date": order_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "order_datetime": order_dt,
                "sales_channel": sales_channel,
                "was_paid": was_paid
            })
            order_id += 1

    print(f"Generated {len(orders)} orders.")

    # -------------------------------------------------------------------------
    # 7. ORDER_DETAIL2 (~20000 rows)
    # -------------------------------------------------------------------------
    bestsellers = [p for p in products if p["sales_tier"] == "bestseller"]
    mid_sellers = [p for p in products if p["sales_tier"] == "mid_seller"]
    low_sellers = [p for p in products if p["sales_tier"] == "low_seller"]

    order_details = []
    detail_id = 1
    items_per_order_dist = [1, 2, 3, 4, 5, 6]
    items_per_order_weights = [0.30, 0.30, 0.20, 0.12, 0.06, 0.02]

    for o in orders:
        num_items = random.choices(items_per_order_dist, weights=items_per_order_weights)[0]
        o_dt = o["order_datetime"]
        o_month = o_dt.month

        for _ in range(num_items):
            tier = random.choices(["bestseller", "mid_seller", "low_seller"], weights=[0.40, 0.55, 0.05])[0]
            
            if o_month in [4, 5, 6, 8, 9] and random.random() < 0.30:
                photo_prods = [p for p in products if p["parent_category_id"] == 4]
                prod = random.choice(photo_prods)
            elif o_month in [10, 11, 12] and random.random() < 0.25:
                poetry_prods = [p for p in products if p["parent_category_id"] == 1]
                prod = random.choice(poetry_prods)
            else:
                if tier == "bestseller":
                    prod = random.choice(bestsellers)
                elif tier == "mid_seller":
                    prod = random.choice(mid_sellers)
                else:
                    prod = random.choice(low_sellers)

            if prod["parent_category_id"] in [3, 6]:
                qty = 1
            else:
                qty = random.choices([1, 2, 3, 4, 5], weights=[0.80, 0.15, 0.03, 0.01, 0.01])[0]

            order_details.append({
                "detail_id": detail_id,
                "order_id": o["id"],
                "product_id": prod["id"],
                "quantity": qty,
                "price": prod["price"]
            })
            detail_id += 1

    print(f"Generated {len(order_details)} order details.")

    # -------------------------------------------------------------------------
    # 8. PAYMENTS (~6000 rows)
    # -------------------------------------------------------------------------
    order_totals = {}
    for od in order_details:
        oid = od["order_id"]
        order_totals[oid] = order_totals.get(oid, 0) + (od["quantity"] * od["price"])

    payments = []
    pay_id = 1

    for o in orders:
        if o["was_paid"] != 1:
            continue

        oid = o["id"]
        o_dt = o["order_datetime"]
        o_date_str = o_dt.strftime("%Y-%m-%d")
        total_price = order_totals.get(oid, 0)

        pay_dt = o_dt + timedelta(days=random.randint(0, 3), minutes=random.randint(1, 60))

        if o["sales_channel"] == "in_person":
            pay_type = random.choices(["card", "cash", "bank_transfer"], weights=[0.55, 0.35, 0.10])[0]
        else:
            pay_type = random.choices(["card", "bank_transfer", "online_gateway"], weights=[0.60, 0.25, 0.15])[0]

        pay_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

        applicable_discounts = []
        for d in discounts:
            if d["active_date"] <= o_date_str <= d["expire_date"]:
                applicable_discounts.append(d)

        is_end_bimonth_day = (o_dt.month in [2, 4, 6, 8, 10, 12]) and (o_dt.day >= 25)
        
        assigned_disc = None
        if is_end_bimonth_day and random.random() < 0.80:
            bimonth_discs = [d for d in applicable_discounts if d["is_bimonthly"]]
            if bimonth_discs:
                assigned_disc = bimonth_discs[0]
        elif applicable_discounts and random.random() < 0.35:
            assigned_disc = random.choice(applicable_discounts)

        if assigned_disc:
            disc_id_val = assigned_disc["id"]
            disc_price = int(round((total_price * (assigned_disc["percentage"] / 100.0)) / 1000.0) * 1000)
        else:
            disc_id_val = None
            disc_price = 0

        total_amount = total_price - disc_price

        payments.append({
            "id": pay_id,
            "order_id": oid,
            "payment_code": pay_code,
            "payment_date": pay_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "payment_type": pay_type,
            "total_price": total_price,
            "discount_id": disc_id_val,
            "discount_price": disc_price,
            "total_amount": total_amount
        })
        pay_id += 1

    print(f"Generated {len(payments)} payments.")

    # -------------------------------------------------------------------------
    # 10. user_basket (~1000 rows)
    # -------------------------------------------------------------------------
    basket_items = []
    recent_cutoff = datetime(2026, 8, 1) - timedelta(days=60)
    basket_candidate_users = []
    
    for u in users:
        weight = 1.0
        if u["is_repeat"]:
            weight *= 3.0
        if u["reg_datetime"] >= recent_cutoff:
            weight *= 1.5
        basket_candidate_users.append((u, weight))

    user_pool = [u for u, w in basket_candidate_users]
    user_weights = [w for u, w in basket_candidate_users]
    
    selected_user_baskets = set()
    while len(selected_user_baskets) < 550:
        picked = random.choices(user_pool, weights=user_weights)[0]
        selected_user_baskets.add(picked["id"])

    for uid in selected_user_baskets:
        num_b_items = random.randint(1, 3)
        for _ in range(num_b_items):
            tier = random.choices(["bestseller", "mid_seller", "low_seller"], weights=[0.50, 0.40, 0.10])[0]
            if tier == "bestseller":
                prod = random.choice(bestsellers)
            elif tier == "mid_seller":
                prod = random.choice(mid_sellers)
            else:
                prod = random.choice(low_sellers)

            qty = random.choices([1, 2, 3, 4], weights=[0.85, 0.12, 0.02, 0.01])[0]
            basket_items.append({
                "user_id": uid,
                "product_id": prod["id"],
                "quantity": qty
            })

    print(f"Generated {len(basket_items)} basket items.")

    # -------------------------------------------------------------------------
    # EXPORT TO SQL FILE (data_output.sql)
    # -------------------------------------------------------------------------
    output_filename = "data_output.sql"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("-- Kohannegar Synthetic Dataset SQL Export\n")
        f.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")

        # 1. Categories
        f.write("-- TABLE: categories\n")
        for c in categories:
            pid = c["parent_id"] if c["parent_id"] is not None else "NULL"
            f.write(f"INSERT INTO categories (id, title, parent_id) VALUES ({c['id']}, '{c['title']}', {pid});\n")
        f.write("\n")

        # 2. Products
        f.write("-- TABLE: products\n")
        for p in products:
            detail_clean = p['detail'].replace("'", "''")
            title_clean = p['title'].replace("'", "''")
            f.write(f"INSERT INTO products (id, title, detail, price, category) VALUES ({p['id']}, '{title_clean}', '{detail_clean}', {p['price']}, {p['category_id']});\n")
        f.write("\n")

        # 3. Users
        f.write("-- TABLE: users\n")
        for u in users:
            f.write(f"INSERT INTO users (id, first_name, last_name, user_name, password, birth_date, city, register_date, disabled) VALUES ({u['id']}, '{u['first_name']}', '{u['last_name']}', '{u['user_name']}', '{u['password']}', '{u['birth_date']}', '{u['city']}', '{u['register_date']}', {u['disabled']});\n")
        f.write("\n")

        # 4. Roles
        f.write("-- TABLE: roles\n")
        for r_id, r_title in roles:
            f.write(f"INSERT INTO roles (id, title) VALUES ({r_id}, '{r_title}');\n")
        f.write("\n")

        # 5. Roles User
        f.write("-- TABLE: roles_user\n")
        for r_id, u_id in roles_user:
            f.write(f"INSERT INTO roles_user (role_id, user_id) VALUES ({r_id}, {u_id});\n")
        f.write("\n")

        # 9. Discount
        f.write("-- TABLE: discount\n")
        for d in discounts:
            title_clean = d['title'].replace("'", "''")
            f.write(f"INSERT INTO discount (id, title, discount_code, active_date, expire_date) VALUES ({d['id']}, '{title_clean}', '{d['discount_code']}', '{d['active_date']}', '{d['expire_date']}');\n")
        f.write("\n")

        # 6. Orders
        f.write("-- TABLE: orders\n")
        for o in orders:
            f.write(f"INSERT INTO orders (id, user_id, order_date, sales_channel, was_paid) VALUES ({o['id']}, {o['user_id']}, '{o['order_date']}', '{o['sales_channel']}', {o['was_paid']});\n")
        f.write("\n")

        # 7. Order Detail 2
        f.write("-- TABLE: order_detail2\n")
        for od in order_details:
            f.write(f"INSERT INTO order_detail2 (order_id, product_id, detail_id, quantity, price) VALUES ({od['order_id']}, {od['product_id']}, {od['detail_id']}, {od['quantity']}, {od['price']});\n")
        f.write("\n")

        # 8. Payments
        f.write("-- TABLE: payments\n")
        for pay in payments:
            disc_val = pay['discount_id'] if pay['discount_id'] is not None else "NULL"
            f.write(f"INSERT INTO payments (id, order_id, payment_code, payment_date, payment_type, total_price, discount_id, discount_price, total_amount) VALUES ({pay['id']}, {pay['order_id']}, '{pay['payment_code']}', '{pay['payment_date']}', '{pay['payment_type']}', {pay['total_price']}, {disc_val}, {pay['discount_price']}, {pay['total_amount']});\n")
        f.write("\n")

        # 10. Basket User
        f.write("-- TABLE: user_basket\n")
        for bu in basket_items:
            f.write(f"INSERT INTO user_basket (user_id, product_id, quantity) VALUES ({bu['user_id']}, {bu['product_id']}, {bu['quantity']});\n")
        f.write("\n")

        f.write("SET FOREIGN_KEY_CHECKS = 1;\n")

    print(f"Successfully generated dataset and exported to '{output_filename}'!")

if __name__ == '__main__':
    main()
