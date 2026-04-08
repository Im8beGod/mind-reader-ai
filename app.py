import streamlit as st

# ---------------- VALUE MAPPING ----------------
def val(x):
    return {
        "HY": 0.95,
        "Y": 0.75,
        "M": 0.5,
        "N": 0.25,
        "HN": 0.05
    }[x]

# ---------------- QUESTIONS ----------------
questions = {
1:"Do they survive exams purely on luck and vibes?",
2:"Are they very chaotic and disorganised?",
3:"Are they likely to have tribal origins?",
4:"Do they send reels/memes very aggressively?",
5:"Is the person likely to scream when a dog appears?",
6:"Do they have to LOOK UP to speak to everyone?",
7:"Do they hide their forehead with their hair?",
8:"Do they take their phone to exam hall?",
9:"Do they talk a lot of nonsense?",
10:"Are they likely to do 'Kaala Jaadu' if you offend them?",
11:"Have they had 'Lafda' with faculties?",
12:"Do they look like The Burj Khalifa?",
13:"Are they likely to disappear if the lights are turned off?",
14:"Would people avoid eye contact with this person?",
15:"Do they look like they use Surf excel as facewash?",
16:"Are they a great politician?",
17:"Does it seem they have their lips stapled?",
18:"Can they make a ponytail out of their hair?",
19:"Do they look like they have not slept in a few days?",
20:"Do they have enough space on their head to project a movie?",
21:"Does their hairline look like it's slowly moving away from its responsibilities?",
22:"Do they talk like they have no mute button?",
23:"Do you need subtitles to understand what they are saying?",
24:"Do they talk so little that even their 'Hmmm' feels like overtime work?",
25:"Do they look like a toothpick?",
26:"Does your person have the personality of a brick wall?",
27:"Do they seem allergic to small talk?",
28:"Can they be considered as brand ambassador of SM (SM paglu)?",
29:"Do they fall in the category of Nibba/Nibbi?",
30:"Do they think they are very smart but compete with PsyDuck in terms of smartness?",
31:"Does the person do something very unique?",
32:"Do they possess in-built bottle opener?",
33:"Do they secretly hate 'Hindi'?",
34:"Are they likely to drink and drive?",
35:"Are they likely to crash their vehicle on a roadtrip?",
36:"Are they real-life NPC?",
37:"Are they likely to be found studying even on their wedding day?",
38:"Will you assume them to be a Taylor Swift fan?",
39:"Will your person be a good 'Mazdoor'?",
40:"Can this person waste an entire day doing absolutely nothing and still sleep peacefully?"
}

# ---------------- DATASET ----------------
probabilities = {
"Nilesh": {1:0.25,2:0.75,3:0.5,4:0.25,5:0.05,6:0.25,7:0.95,8:0.25,9:0.75,10:0.95,11:0.75,12:0.5,13:0.95,14:0.25,15:0.25,16:0.75,17:0.25,18:0.25,19:0.5,20:0.95,21:0.95,22:0.75,23:0.25,24:0.25,25:0.05,26:0.25,27:0.75,28:0.75,29:0.25,30:0.5,31:0.75,32:0.25,33:0.25,34:0.25,35:0.95,36:0.05,37:0.25,38:0.25,39:0.25,40:0.75},

"Vaibhav": {1:0.25,2:0.75,3:0.5,4:0.25,5:0.25,6:0.05,7:0.5,8:0.25,9:0.75,10:0.25,11:0.75,12:0.75,13:0.25,14:0.75,15:0.5,16:0.25,17:0.25,18:0.95,19:0.5,20:0.95,21:0.95,22:0.75,23:0.25,24:0.25,25:0.75,26:0.25,27:0.25,28:0.75,29:0.5,30:0.25,31:0.25,32:0.25,33:0.25,34:0.5,35:0.5,36:0.25,37:0.05,38:0.5,39:0.95,40:0.75}
}

# ---------------- ENGINE ----------------
def best_question(scores, asked):
    best_q = None
    best_var = -1

    for q in questions:
        if q in asked:
            continue

        vals = [probabilities[p][q] for p in scores]
        mean = sum(vals)/len(vals)
        var = sum((v-mean)**2 for v in vals)

        if var > best_var:
            best_var = var
            best_q = q

    return best_q

# ---------------- SESSION ----------------
if "scores" not in st.session_state:
    st.session_state.scores = {p:1.0 for p in probabilities}
    st.session_state.asked = []
    st.session_state.count = 0

# ---------------- UI ----------------
st.title("🧠 Mind Reader 😈")

q = best_question(st.session_state.scores, st.session_state.asked)

if q:
    st.subheader(questions[q])

    cols = st.columns(5)
    options = ["HY","Y","M","N","HN"]

    for i, opt in enumerate(options):
        if cols[i].button(opt):

            user_val = val(opt)

            for p in st.session_state.scores:
                sim = 1 - abs(probabilities[p][q] - user_val)
                st.session_state.scores[p] *= sim

            # normalize
            total = sum(st.session_state.scores.values())
            for p in st.session_state.scores:
                st.session_state.scores[p] /= total

            st.session_state.asked.append(q)
            st.session_state.count += 1

            sorted_p = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)

            if len(sorted_p) > 1 and (sorted_p[0][1] - sorted_p[1][1] > 0.25 or st.session_state.count >= 12):
                st.success(f"😈 I KNOW IT... It's {sorted_p[0][0]}")
            else:
                st.rerun()
