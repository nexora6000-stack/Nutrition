import streamlit as st

import nutrition as nu

st.set_page_config(page_title="Project Nutrition", page_icon="🥗", layout="centered")
st.title("Project Nutrition")
st.caption("Build a 7-day meal plan from your profile, diet, allergies and cuisine preferences.")
st.warning(
    f"**Prototype, not medical advice.** Nutrition values and allergen tags are approximate and "
    f"cover only {len(nu.MEALS)} illustrative dishes. Ingredients and cross-contamination are not "
    "checked. If you have a severe allergy, a medical condition, or are under 18, speak to a doctor "
    "or registered dietitian and verify every meal yourself."
)

with st.form("profile"):
    c1, c2, c3 = st.columns(3)
    age = c1.number_input("Age", 1, 120, 30)
    sex = c2.selectbox("Sex (for the formula)", ["Male", "Female"])
    height = c3.number_input("Height (cm)", 50, 260, 170)
    c4, c5, c6 = st.columns(3)
    weight = c4.number_input("Weight (kg)", 20, 400, 70)
    activity = c5.selectbox("Activity", list(nu.ACTIVITY), index=1)
    goal = c6.selectbox("Goal", ["Lose weight", "Maintain", "Build muscle"], index=1)

    allergies = st.multiselect("Allergies (hard filter)", list(nu.ALLERGENS),
                               format_func=nu.ALLERGENS.get)
    diet = st.selectbox("Diet", list(nu.DIETS))
    dislikes = st.text_input("Dislikes (comma-separated ingredients)", placeholder="e.g. mushroom, olives")
    cuisines = st.multiselect(
        "Cuisines you prefer", list(nu.CUISINES), format_func=nu.CUISINES.get,
        help="None selected means all. If a slot has no match, the plan widens to other cuisines. "
             "It never relaxes allergy, diet or dislike filters.")
    submitted = st.form_submit_button("Build my 7-day plan", type="primary")

if submitted:
    error = nu.validate(age, height, weight)
    if error:
        st.session_state.pop("result", None)
        st.error(error)
    else:
        t = nu.targets(age, "m" if sex == "Male" else "f", height, weight, nu.ACTIVITY[activity],
                       {"Lose weight": "lose", "Maintain": "maintain", "Build muscle": "build"}[goal])
        plan = nu.make_plan(t, allergies, diet, dislikes.split(","), cuisines)
        st.session_state["result"] = (t, plan)

if "result" in st.session_state:
    t, plan = st.session_state["result"]
    st.subheader("Your daily targets")
    cols = st.columns(4)
    for col, (label, val, unit) in zip(cols, [("Calories", t["kcal"], "kcal"), ("Protein", t["protein"], "g"),
                                              ("Carbs", t["carbs"], "g"), ("Fat", t["fat"], "g")]):
        col.metric(label, f"{val} {unit}")
    if t["note"]:
        st.info(t["note"])

    missing = [nu.SLOTS[e["slot"]].lower() for e in plan[0] if e["meal"] is None]
    if missing:
        st.error(f"**No safe option for: {', '.join(missing)}.** Nothing in the database passes your "
                 "allergy, diet and dislike filters. The tool will not relax those filters. "
                 "Remove a dislike or ask a dietitian for suggestions.")

    st.subheader("7-day plan")
    for tab, day in zip(st.tabs(nu.DAYS), plan):
        with tab:
            for e in day:
                label = nu.SLOTS[e["slot"]]
                m = e["meal"]
                if m is None:
                    st.markdown(f"**{label}** — :red[No safe option found]")
                    continue
                st.markdown(f"**{label}: {m.name}**")
                st.caption(f"{e['kcal']:.0f} kcal · portion ×{e['portion']:.2f} · P {e['protein']:.0f} g · "
                           f"C {e['carbs']:.0f} g · F {e['fat']:.0f} g · fibre {e['fibre']:.0f} g")
                tags = [f":red[Contains {nu.ALLERGENS[c].lower()}]" for c in m.allergens]
                st.markdown(" ".join(tags) if tags else ":gray[None of the 8 tracked allergens]")
                if e["widened"]:
                    st.markdown(":gray[Outside your preferred cuisines]")
            tot = nu.day_totals(day)
            st.divider()
            st.markdown("**Daily total vs target**")
            for label, key, unit in [("Calories", "kcal", "kcal"), ("Protein", "protein", "g"),
                                     ("Carbs", "carbs", "g"), ("Fat", "fat", "g")]:
                st.progress(min(1.0, tot[key] / t[key]), text=f"{label}: {tot[key]:.0f} / {t[key]} {unit}")
            if abs(tot["kcal"] - t["kcal"]) > t["kcal"] * 0.1:
                st.caption("Total is more than 10% from target because portions are limited to "
                           "0.6–1.6× and the meal pool is small.")
