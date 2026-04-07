import sys
import random
import time
import os

# ========================
# GAME STATE
# ========================

deliveries_done = 0
money = 100
drugs = 0
seeds = 0
growing_solution = 0

day = 1
risk = 0
reputation = 0
in_jail = False
jail_days = 0
workers = 0
level = 1
xp = 0
xp_needed = 100
max_production = 5
jail_rep_used = False
jail_train_used = False
jail_lawyer_used = False
daily_customers = []
customers_left_today = 0

territories = {
    "Downtown": {"profit": (40, 80), "risk": 25},
    "Suburbs": {"profit": (20, 40), "risk": 10},
    "Industrial": {"profit": (30, 60), "risk": 18}
}

upgrades = {
    "Safe House": False,
    "Police Bribe": False,
    "Chemist": False
}

# ========================
# PRINT FUNCTIONS
# ========================

def slow_print(text, delay=0.05):
    for letter in text:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def very_slow_print(text, delay=0.07):
    for letter in text:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ========================
# SAVE SYSTEM
# ========================

def save_game():
    with open("save.txt", "w") as f:
        f.write(f"{day}\n{money}\n{drugs}\n{seeds}\n{growing_solution}\n")
        f.write(f"{risk}\n{reputation}\n{deliveries_done}\n")
        f.write(f"{max_production}\n")
        for key in upgrades:
            f.write(f"{upgrades[key]}\n")
    slow_print("Game Saved.")

def load_game():
    global day, money, drugs, seeds, growing_solution
    global risk, reputation, deliveries_done, max_production

    if not os.path.exists("save.txt"):
        return False

    with open("save.txt", "r") as f:
        lines = f.read().splitlines()

    day = int(lines[0])
    money = int(lines[1])
    drugs = int(lines[2])
    seeds = int(lines[3])
    growing_solution = int(lines[4])
    risk = int(lines[5])
    reputation = int(lines[6])
    deliveries_done = int(lines[7])
    max_production = int(lines[8])

    upgrades["Safe House"] = lines[9] == "True"
    upgrades["Police Bribe"] = lines[10] == "True"
    upgrades["Chemist"] = lines[11] == "True"

    slow_print("Save Loaded.")
    return True

# ========================
# QUIT SYSTEM
# ========================

def quit_game():
    choice = input("Are you sure you want to quit? (y/n): ")
    if choice.lower() == "y":
        save_game()
        slow_print("Exiting game...")
        sys.exit()
# ========================
# JAIL SYSTEM
# ========================

def check_for_arrest():
    global risk, in_jail, jail_days, money, drugs

    if risk >= 100 and not in_jail:
        slow_print("Police raided your base!")
        slow_print("You got arrested!")

        in_jail = True
        jail_days = random.randint(2, 5)

        # Optional punishment
        lost_money = int(money * 0.3)
        money -= lost_money

        lost_drugs = min(drugs, 3)
        drugs -= lost_drugs

        slow_print(f"You lost ${lost_money} and {lost_drugs} drugs.")
        risk = 0
# ========================
# CUSTOMER SYSTEM
# ========================

def generate_customers():
    global daily_customers, customers_left_today

    possible_customers = [
        "Tom.", "Jeff.", "Jose.", "El Chapo.",
        "Mike.", "Ali.", "Viktor.", "Sam.",
        "Carlos.", "Jamal."
    ]

    amount = random.randint(3, 5)
    daily_customers = random.sample(possible_customers, amount)
    customers_left_today = len(daily_customers)

def get_next_customer():
    global customers_left_today
    if customers_left_today > 0:
        customers_left_today -= 1
        return daily_customers[customers_left_today]
    return None

# ========================
# MAIN MENU
# ========================

def main_menu():
    while True:
        print("\n" + "=" * 30)
        slow_print("MAIN MENU")
        print("=" * 30)
        print("1. Start Game")
        print("2. Load Game")
        print("3. How to Play")
        print("4. Credits")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            start_game()
        elif choice == "2":
            if load_game():
                generate_customers()
                base_menu()
            else:
                slow_print("No save file found.")
        elif choice == "3":
            how_to_play()
        elif choice == "4":
            credits()
        elif choice == "5":
            quit_game()

# ========================
# START GAME
# ========================

def start_game():
    generate_customers()

    slow_print("\nStarting the game...")
    org_name = input("Enter your organization name: ")

    slow_print("You are a low life criminal starting a new drug business.")
    slow_print("You find yourself in a city with no money, health problems, and illegal immigrants.")
    slow_print("After 3 rough days with no food you meet Uncle Bob who is a former drug dealer.")
    slow_print("Uncle bob leads you to his old garage and told you to use it as a base.")
    slow_print("You reach Uncle Bob's garage which to your suprise is pretty clean.")

    base_menu()

# ========================
# BASE
# ========================

def base_menu():
    global day
    while True:
        if in_jail:
            print("\n====== JAIL ======")
            print(f"Days remaining: {jail_days}")
            if not jail_train_used:
               print("1. Train")
            if not jail_rep_used:
               print("2. Build Reputation")
            if not jail_lawyer_used:
               print("3. Call Lawyer ($100)")
            print("4. Sleep")
            print("0. Quit Game")

            choice = input("Choose: ")

            if choice == "1":
                jail_train()
            elif choice == "2":
                jail_reputation()
            elif choice == "3":
                jail_lawyer()
            elif choice == "4":
                sleep()
            elif choice == "0":
                quit_game()

            continue
        print("\n====== BASE ======")
        print(f"Day: {day} | Level: {level} | XP: {xp}/{xp_needed}")
        print(f"Money: ${money} | Drugs: {drugs} | Risk: {risk}% | Rep: {reputation}")
        print("1. Hop on the computer.")
        print("2. Go to the city.")
        print("3. Drug Station.")
        print("4. Sleep.")
        print("5. Save Game")
        print("0. Quit Game")

        choice = input("Choose: ")

        if choice == "1":
            desktop()
        elif choice == "2":
            city()
        elif choice == "3":
            drug_station()
        elif choice == "4":
            sleep()
        elif choice == "5":
            save_game()
        elif choice == "0":
            quit_game()

# ========================
# LEVEL SYSTEM
# ========================

def add_xp(amount):
    global xp, level, xp_needed

    xp += amount
    slow_print(f"You gained {amount} XP!")

    while xp >= xp_needed:
        xp -= xp_needed
        level += 1
        xp_needed += 50

        slow_print("LEVEL UP!")
        slow_print(f"You are now Level {level}!")

        level_up_bonus()
def level_up_bonus():
    global reputation

    reputation += 5
    slow_print("Your reputation increased by 5!")

# ========================
# WORKER SYSTEM
# ========================

def city_hire_worker():
    global money, workers

    cost = 200

    print("\n====== HIRE WORKER ======")
    print(f"Current Workers: {workers}")
    print(f"Hiring Cost: ${cost}")
    print("1. Hire")
    print("2. Cancel")

    choice = input("Choose: ")

    if choice == "1":
        if money >= cost:
            money -= cost
            workers += 1
            slow_print("You hired a worker from the city.")
        else:
            slow_print("Not enough money.")

def worker_production():
    global drugs, workers

    if workers > 0:
        produced = workers  # 1 drug per worker per day
        drugs += produced
        slow_print(f"Your {workers} workers produced {produced} drugs.")
# ========================
# SLEEP SYSTEM
# ========================

def sleep():
    global day, risk, in_jail, jail_days

    slow_print("You go to sleep...")
    day += 1
    global jail_rep_used, jail_train_used, jail_lawyer_used
    jail_rep_used = False
    jail_train_used = False
    jail_lawyer_used = False
    if in_jail:
        jail_days -= 1
        slow_print(f"You are in jail. {jail_days} days remaining.")

        if jail_days <= 0:
            in_jail = False
            slow_print("You were released from jail.")
    else:
        risk = max(0, risk - 20)
        worker_production()  # if you added workers
        check_for_arrest()

    generate_customers()
    save_game()
    slow_print("A new day begins.")
# ========================
# JAIL ACTIVITIES
# ========================

def jail_train():
    global risk, jail_train_used

    if jail_train_used:
        slow_print("You already trained today.")
        return

    slow_print("You train in the prison yard.")
    reduction = random.randint(5, 15)
    risk = max(0, risk - reduction)

    jail_train_used = True

    slow_print(f"Future risk reduced by {reduction}%.")

def jail_reputation():
    global reputation, jail_rep_used

    if jail_rep_used:
        slow_print("You already built reputation today.")
        return

    gain = random.randint(1, 5)
    reputation += gain
    jail_rep_used = True
    slow_print(f"You gained {gain} reputation in prison.")

def jail_lawyer():
    global money, jail_days, jail_lawyer_used

    if jail_lawyer_used:
        slow_print("You already called your lawyer today.")
        return

    if money >= 100:
        money -= 100
        reduction = random.randint(1, 2)
        jail_days = max(0, jail_days - reduction)

        jail_lawyer_used = True

        slow_print(f"Lawyer reduced sentence by {reduction} days.")
    else:
        slow_print("Not enough money.")
# ========================
# DRUG STATION
# ========================

def drug_station():
    global drugs, seeds, growing_solution, max_production

    print("\n====== DRUG STATION ======")
    print(f"Seeds: {seeds} | Growing Solution: {growing_solution}")
    print(f"Max Production Per Visit: {max_production}")
    print("1. Make Drugs")
    print("2. Return")
    print("0. Quit Game")

    choice = input("Choose: ")

    if choice == "1":
        try:
            amount = int(input("How many drugs do you want to make? "))
        except ValueError:
            slow_print("Please enter a valid number")
            return
        
        if amount > max_production:
            slow_print(f"You can only produce up to {max_production} at once.")
            return

        if seeds >= amount and growing_solution >= amount:
            seeds -= amount
            growing_solution -= amount

            produced = amount * (2 if upgrades["Chemist"] else 1)
            drugs += produced

            slow_print(f"You produced {produced} drugs.")
        else:
            slow_print("Not enough materials.")

    elif choice == "0":
        quit_game()

# ========================
# DESKTOP
# ========================

def desktop():
    while True:
        print("\n====== DESKTOP ======")
        print("1. Emails")
        print("2. Drugzon")
        print("3. Shutdown")
        print("0. Quit Game")

        choice = input("Choose: ")

        if choice == "1":
            emails()
        elif choice == "2":
            store()
        elif choice == "3":
            break
        elif choice == "0":
            quit_game()

# ========================
# STORE
# ========================

def store():
    global money, seeds, growing_solution

    while True:
        print("\n====== ONLINE STORE ======")
        print(f"Money: ${money}")
        print("1. Buy Seeds ($10 each)")
        print("2. Buy Growing Solution ($15 each)")
        print("3. Exit")
        print("0. Quit Game")

        choice = input("Choose: ")

        # BUY SEEDS
        if choice == "1":
            try:
                amount = int(input("How many seeds do you want to buy? "))
                total_cost = amount * 10

            except ValueError:
                slow_print("Please enter a valid number")
                return
        

            if money >= total_cost:
                money -= total_cost
                seeds += amount
                slow_print(f"You bought {amount} seeds.")
            else:
                slow_print("Not enough money.")

        # BUY GROWING SOLUTION
        elif choice == "2":
            try:
                amount = int(input("How many growing solutions do you want to buy? "))
                total_cost = amount * 15
            except ValueError:
                slow_print("Please enter a valid number.")
                return

            if money >= total_cost:
                money -= total_cost
                growing_solution += amount
                slow_print(f"You bought {amount} growing solutions.")
            else:
                slow_print("Not enough money.")

        elif choice == "3":
            return

        elif choice == "0":
            quit_game()

        else:
            slow_print("Invalid Input")

# ========================
# EMAIL SYSTEM
# ========================

def emails():
    global deliveries_done, drugs, money, reputation

    customer = get_next_customer()

    if customer is None:
        slow_print("No more customers today.")
        return

    print("\n====New Email====")
    slow_print(f"From: {customer}")
    slow_print("Subject: Drugs")

    print("1. Send")
    print("2. Ignore")
    print("0. Quit Game")

    choice = input("Choose: ")

    if choice == "1":
        if drugs > 0:
            drugs -= 1
            earned = random.randint(30, 50)
            money += earned
            add_xp(20)
            deliveries_done += 1
            reputation += 2
            slow_print(f"Earned ${earned}")
        else:
            slow_print("No drugs available.")
    elif choice == "0":
        quit_game()

# ========================
# CITY
# ========================

def city():
    while True:
        if in_jail:
            return
        print("\n======= CITY =======")
        print("1. Street Deal")
        print("2. Visit Supplier")
        print("3. Black Market")
        print("4. Upgrade Base")
        print("5. Hire Worker")
        print("6. Return")
        print("0. Quit Game")
        choice = input("Choose: ")

        if choice == "1":
            street_deal()
        elif choice == "2":
            supplier()
        elif choice == "3":
            black_market()
        elif choice == "4":
            upgrade_menu()
        elif choice == "5":
            city_hire_worker()
        elif choice == "6":
            return
        elif choice == "0":
            quit_game()

# ========================
# STREET DEAL
# ========================
def police_event():
    global drugs, money, risk

    slow_print("Police spotted you!")

    if random.randint(1, 100) < 50:
        lost = min(drugs, 2)
        drugs -= lost
        slow_print(f"You dropped {lost} drugs escaping!")
    else:
        fine = min(money, 50)
        money -= fine
        slow_print(f"You paid ${fine} fine.")

    risk += 15
    check_for_arrest()
def street_deal():
    global drugs, money, risk, reputation

    if drugs <= 0:
        slow_print("You have no drugs.")
        return

    areas = list(territories.keys())

    print("\nChoose Territory:")
    for i, area in enumerate(areas):
        print(f"{i+1}. {area}")

    # SAFE INPUT PROTECTION
    try:
        choice = int(input("Choose territory: ")) - 1
        if choice < 0 or choice >= len(areas):
            slow_print("Invalid territory.")
            return
    except ValueError:
        slow_print("Please enter a valid number.")
        return

    area = areas[choice]
    data = territories[area]
    chance = random.randint(1, 100)

    if chance < 60:
        profit = random.randint(*data["profit"])
        drugs -= 1
        money += profit
        add_xp(25)
        reputation += 3

        risk_gain = data["risk"]
        if upgrades["Police Bribe"]:
            risk_gain = int(risk_gain * 0.7)

        risk += risk_gain
        check_for_arrest()

        slow_print(f"Sold for ${profit}")

    elif chance < 85:
        slow_print("No customers found.")
        risk += 5
        check_for_arrest()

    else:
        police_event()

# ========================
# SUPPLIER
# ========================

def supplier():
    global money, seeds
    price = random.randint(5, 12)
    print(f"Supplier offers Seeds for ${price}")
    choice = input("Buy? (y/n): ")
    if choice.lower() == "y" and money >= price:
        money -= price
        seeds += 1

# ========================
# BLACK MARKET
# ========================

def black_market():
    global drugs, money, risk

    if reputation < 20:
        slow_print("You are not known enough.")
        return

    if drugs > 0:
        profit = random.randint(80, 120)
        drugs -= 1
        money += profit
        add_xp(40)
        risk += 30
        check_for_arrest()
        slow_print(f"Black Market Sale: ${profit}")

# ========================
# UPGRADES
# ========================

def upgrade_menu():
    global money, max_production

    print("\n====== UPGRADES ======")
    print("1. Safe House ($200)")
    print("2. Police Bribe ($150)")
    print("3. Hire Chemist ($300)")
    print("4. Production Upgrade ($250)")
    print("5. Exit")

    choice = input("Choose: ")

    if choice == "1" and money >= 200:
        money -= 200
        upgrades["Safe House"] = True

    elif choice == "2" and money >= 150:
        money -= 150
        upgrades["Police Bribe"] = True

    elif choice == "3" and money >= 300:
        money -= 300
        upgrades["Chemist"] = True

    elif choice == "4" and money >= 250:
        money -= 250
        max_production += 5
        slow_print("Production capacity increased by 5!")

    elif choice == "5":
        return

# ========================
# HOW TO PLAY & CREDITS
# ========================

def how_to_play():
    slow_print("\nHow to Play:")
    slow_print("- Make choices by typing numbers")
    slow_print("- Grow drugs at base")
    slow_print("- Sell in city")
    slow_print("- Manage risk and reputation")
    input("Press Enter...")

def credits():
    print("\n========Credits=======")
    very_slow_print("\nAll rights are reserved to Don'tDoDrugs.com(DDD.com)")
    very_slow_print("Developers: Wahbi Bakbak, and Younes Alaska")
    input("Press Enter...")

# ========================
# START
# ========================

slow_print("\nDrugs r not cool")
slow_print("\nBy: Don'tDoDrugs.com")

main_menu()