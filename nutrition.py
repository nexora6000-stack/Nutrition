"""Project Nutrition: meal data, targets and 7-day planner (no UI code here).

Run `python nutrition.py` to execute the safety self-test.
"""
from dataclasses import dataclass

ALLERGENS = {"N": "Tree nuts/peanuts", "D": "Dairy", "G": "Gluten", "E": "Egg",
             "S": "Soy", "T": "Sesame", "C": "Shellfish", "F": "Fish"}
CUISINES = {"M": "Mediterranean", "S": "South Asian", "E": "East Asian", "L": "Latin American"}
SLOTS = {"B": "Breakfast", "L": "Lunch", "D": "Dinner", "S": "Snack"}
SHARE = {"B": 0.25, "L": 0.35, "D": 0.30, "S": 0.10}
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
ACTIVITY = {"Mostly sitting": 1.2, "Light (1-3 days/week)": 1.375,
            "Moderate (3-5 days/week)": 1.55, "Very active (6-7 days/week)": 1.725}
# diet code: v vegan, g vegetarian, p pescatarian, h halal-friendly meat, x non-halal
DIETS = {"Omnivore": "vgphx", "Pescatarian": "vgp", "Vegetarian": "vg", "Vegan": "v", "Halal": "vgph"}


@dataclass(frozen=True)
class Meal:
    name: str
    cuisine: str
    slot: str
    kcal: float
    protein: float
    carbs: float
    fat: float
    fibre: float
    allergens: str
    diet: str
    ingredients: str


# name|cuisine|slot|kcal|protein|carb|fat|fibre|allergens|diet|ingredients
_RAW = """Greek yogurt with honey and walnuts|M|B|350|20|35|14|3|DN|g|yogurt,honey,walnuts
Shakshuka with whole-wheat pita|M|B|420|20|40|18|8|EG|g|egg,tomato,pepper,pita
Oats with berries and almond milk|M|B|330|10|55|8|9|GN|v|oats,berries,almond milk
Chickpea-flour pancake (besan chilla)|S|B|300|16|36|9|8||v|chickpea flour,onion,tomato,spinach
Vegetable poha with peanuts|S|B|340|8|55|10|5|N|v|flattened rice,peas,peanuts,onion
Egg bhurji with roti|S|B|380|18|36|17|6|EG|g|egg,onion,tomato,roti
Rice congee with egg and scallion|E|B|320|14|48|7|2|E|g|rice,egg,scallion,ginger
Tofu scramble with toast|E|B|360|20|34|15|6|SG|v|tofu,spinach,mushroom,bread
Black bean and avocado arepa|L|B|420|13|52|18|12||v|corn flour,black beans,avocado
Huevos rancheros bowl|L|B|400|19|38|19|9|E|g|egg,corn tortilla,beans,salsa
Smoked salmon and egg toast|A|B|390|27|30|16|4|EGF|p|salmon,egg,rye bread,cucumber
Peanut butter banana smoothie|A|B|380|16|50|14|6|N|v|banana,peanut butter,oat milk
Lentil soup with whole-grain bread|M|L|420|22|65|8|16|G|v|lentils,carrot,onion,bread
Grilled chicken with quinoa tabbouleh|M|L|510|42|45|16|7||h|chicken,quinoa,parsley,tomato
Tuna Nicoise salad|M|L|460|34|28|24|6|EF|p|tuna,egg,green beans,olives,potato
Falafel plate with hummus|M|L|540|20|58|26|13|TG|v|chickpeas,tahini,pita,cucumber
Chana masala with brown rice|S|L|520|20|82|12|16||v|chickpeas,tomato,onion,brown rice
Chicken tikka with dal and salad|S|L|530|44|42|18|9|D|h|chicken,yogurt,lentils,cucumber
Paneer palak with roti|S|L|560|26|50|28|9|DG|g|paneer,spinach,roti
Chicken and vegetable stir-fry with rice|E|L|500|38|58|12|5|SG|h|chicken,broccoli,rice,soy sauce
Tofu and chili-bean stew with rice|E|L|480|20|60|17|5|SG|v|tofu,rice,chili bean paste,scallion
Shrimp and vegetable rice bowl|E|L|470|30|58|11|5|CSG|p|shrimp,rice,carrot,bok choy,soy sauce
Chicken burrito bowl|L|L|580|40|65|16|13||h|chicken,rice,black beans,corn,salsa
Lentil and sweet potato tacos|L|L|480|18|75|11|14||v|lentils,sweet potato,corn tortilla,cabbage
Pork and pineapple tacos|L|L|520|32|48|20|6||x|pork,pineapple,corn tortilla,onion
Baked salmon with roasted vegetables|M|D|520|38|30|26|7|F|p|salmon,zucchini,potato,olive oil
Chicken souvlaki with Greek salad|M|D|540|45|30|24|5|D|h|chicken,feta,tomato,cucumber
White bean and kale stew|M|D|430|20|62|10|15||v|white beans,kale,tomato,carrot
Whole-wheat pasta primavera|M|D|480|16|72|14|8|GD|g|pasta,zucchini,tomato,parmesan
Fish curry with rice|S|D|520|34|58|16|4|F|p|fish,coconut milk,tomato,rice
Vegetable biryani with raita|S|D|540|14|82|16|6|D|g|rice,peas,carrot,yogurt
Dal tadka with roti|S|D|470|20|68|12|13|G|v|lentils,tomato,onion,roti
Teriyaki salmon with rice and greens|E|D|540|36|58|16|4|FSG|p|salmon,rice,bok choy,soy sauce
Tofu and mushroom noodle stir-fry|E|D|500|24|68|14|6|SG|v|tofu,mushroom,noodles,soy sauce
Beef and broccoli with rice|E|D|520|34|58|16|5|SG|h|beef,broccoli,rice,soy sauce
Grilled fish tacos|L|D|480|32|50|16|8|F|p|white fish,corn tortilla,cabbage,lime
Black bean stuffed peppers|L|D|420|18|60|11|14||v|black beans,peppers,rice,corn
Chicken and rice with plantain|L|D|560|40|65|14|6||h|chicken,rice,plantain,peppers
Turkey and bean chili|A|D|450|38|42|13|13||h|turkey,kidney beans,tomato,onion
Apple with almond butter|A|S|200|5|22|11|5|N|v|apple,almond butter
Hummus and carrot sticks|M|S|160|6|18|8|5|T|v|hummus,carrot,tahini
Roasted chickpeas|S|S|170|9|24|4|7||v|chickpeas,spices
Edamame with sea salt|E|S|150|13|12|6|5|S|v|edamame
Fruit and yogurt cup|A|S|180|10|28|3|3|D|g|yogurt,mixed fruit
Guacamole with corn chips|L|S|210|3|20|14|6||v|avocado,corn chips,lime
Boiled egg and cucumber|A|S|110|9|3|7|1|E|g|egg,cucumber"""


def _load():
    meals = []
    for line in _RAW.splitlines():
        a = line.split("|")
        meals.append(Meal(a[0], a[1], a[2], *map(float, a[3:8]), a[8], a[9], a[10]))
    return meals


MEALS = _load()


def validate(age, height, weight):
    """Return an error message, or None if the inputs are usable."""
    if age < 18:
        return ("This planner is for adults (18 and over). Calorie needs change as children "
                "and teenagers grow, so please talk to a doctor or registered dietitian.")
    if not (18 <= age <= 80 and 120 <= height <= 220 and 35 <= weight <= 250):
        return ("Those values are outside the range this formula is meant for "
                "(age 18-80, height 120-220 cm, weight 35-250 kg). "
                "A health professional can give a safer estimate.")
    return None


def targets(age, sex, height, weight, activity, goal):
    """Mifflin-St Jeor. sex is 'm' or 'f'; goal is 'lose', 'maintain' or 'build'."""
    bmr = 10 * weight + 6.25 * height - 5 * age + (5 if sex == "m" else -161)
    tdee = bmr * activity
    if goal == "lose":
        kcal = tdee - min(500, tdee * 0.2)
    elif goal == "build":
        kcal = tdee * 1.1
    else:
        kcal = tdee
    floor = 1500 if sex == "m" else 1200
    note = ""
    if kcal < floor:
        kcal = floor
        note = (f"Your calculated target was below the {floor} kcal minimum this tool allows "
                "without medical supervision, so it was raised to that minimum.")
    kcal = round(kcal / 10) * 10
    protein = min(weight * (1.4 if goal == "maintain" else 1.8), 0.35 * kcal / 4)
    fat = 0.25 * kcal / 9
    carbs = (kcal - protein * 4 - fat * 9) / 4
    return {"kcal": kcal, "protein": round(protein), "carbs": round(carbs),
            "fat": round(fat), "note": note}


def pool(slot, allergies, diet, dislikes, cuisines):
    """Return (meals, widened). Allergy, diet and dislike filters are hard limits.
    Only the cuisine preference may be widened."""
    terms = [t.strip().lower() for t in dislikes if len(t.strip()) > 1]
    base = [m for m in MEALS
            if m.slot == slot
            and not (set(m.allergens) & set(allergies))
            and m.diet in DIETS[diet]
            and not any(t in f"{m.name} {m.ingredients}".lower() for t in terms)]
    if not cuisines:
        return base, False
    preferred = [m for m in base if m.cuisine in cuisines]
    if preferred:
        return preferred, False
    return base, bool(base)


def make_plan(t, allergies, diet, dislikes, cuisines):
    pools = {s: pool(s, allergies, diet, dislikes, cuisines) for s in SLOTS}
    plan = []
    for d in range(7):
        day = []
        for si, s in enumerate(SLOTS):
            meals, widened = pools[s]
            if not meals:
                day.append({"slot": s, "meal": None})
                continue
            goal = t["kcal"] * SHARE[s]
            top = sorted(meals, key=lambda m: abs(m.kcal - goal))[:5]
            m = top[(d + si) % len(top)]
            x = round(max(0.6, min(1.6, goal / m.kcal)) * 20) / 20
            day.append({"slot": s, "meal": m, "portion": x, "widened": widened,
                        "kcal": m.kcal * x, "protein": m.protein * x, "carbs": m.carbs * x,
                        "fat": m.fat * x, "fibre": m.fibre * x})
        plan.append(day)
    return plan


def day_totals(day):
    keys = ("kcal", "protein", "carbs", "fat", "fibre")
    return {k: sum(e[k] for e in day if e["meal"]) for k in keys}


def _self_test():
    """Check every allergen combination x every diet: no unsafe meal may ever appear."""
    codes, n = list(ALLERGENS), 0
    t = targets(30, "m", 175, 70, 1.375, "maintain")
    for diet in DIETS:
        for mask in range(1 << len(codes)):
            sel = [c for i, c in enumerate(codes) if mask >> i & 1]
            for day in make_plan(t, sel, diet, [], ["M"]):
                for e in day:
                    m = e["meal"]
                    if m:
                        assert not set(m.allergens) & set(sel), (diet, sel, m.name)
                        assert m.diet in DIETS[diet], (diet, m.name)
                        n += 1
    assert targets(40, "f", 150, 40, 1.2, "lose")["kcal"] >= 1200
    assert validate(16, 170, 60) is not None
    print(f"Self-test passed: {n} meal placements checked, no unsafe meals.")


if __name__ == "__main__":
    _self_test()
