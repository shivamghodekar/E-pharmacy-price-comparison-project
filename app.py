import streamlit as st
import serpapi
import pandas as pd
import matplotlib.pyplot as plt

def compare(name):
    params = {
        "engine": "google_shopping",
        "q": name,
        "api_key": "9c2cbb19660179906034688c9b31d28ecb6f8129754f7683849558ee663f523e",
        "gl": "in"
    }

    search = serpapi.GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results["shopping_results"]
    return (shopping_results)


# header
c1, c3 = st.columns(2)
c1.image("e_pharmacy.png", width=200)
c3.header("E-Pharmacy Price compairsion system")


st.sidebar.title("Enter name of medicine")
st.sidebar.markdown(" ")
st.sidebar.markdown(" ")


medicine_name = st.sidebar.text_input("Enter name of medicine")
number = st.sidebar.number_input('Enter number of option', min_value=1, max_value=10, value=3)
#number = st.sidebar.text_input("Enter The Number of options")
med_name = []
med_price = []

if medicine_name is not None:
    if st.sidebar.button("Price Compare"):

        inline_shopping_results = compare(medicine_name)
        st.sidebar.image(inline_shopping_results[0].get("thumbnail"))
        lowest_price = float(inline_shopping_results[0].get("price")[1:])
        lowest_price_index = 0

        for i in range(int(number)):
            st.title(f"Option {i + 1}")
            c1, c2 = st.columns(2)
            curent_price = float(inline_shopping_results[i].get("price")[1:])
            med_name.append(inline_shopping_results[i].get("source"))
            med_price.append(float((inline_shopping_results[i].get("price"))[1:10]))

            c1.write("Company ")
            c2.write(inline_shopping_results[i].get("source"))

            c1.write("Medicine Name")
            c2.write((inline_shopping_results[i].get("title"))[0:40])

            print(curent_price)
            print(lowest_price)
            lowest_price = min(curent_price, lowest_price)
            print(lowest_price)
            if curent_price <= lowest_price:
                lowest_price = curent_price
                print(lowest_price)
                lowest_price_index = i
                print(lowest_price_index)

            c1.write("Price")
            c2.write(inline_shopping_results[i].get("price"))

            url = inline_shopping_results[i].get("product_link")
            print(url)
            c1.write("BUY LINK ")
            c2.write("[link](%s)" % url)


        st.title("Best Option ")
        i = lowest_price_index
        c1, c2 = st.columns(2)
        c1.write("Company ")
        c2.write(inline_shopping_results[i].get("source"))

        c1.write("Price")
        c2.write(inline_shopping_results[i].get("price"))

        url = inline_shopping_results[i].get("product_link")
        print(url)
        c1.write("BUY LINK ")
        c2.write("[link](%s)" % url)


        # graph comrasion
        df = pd.DataFrame(med_price, med_name)
        st.title("Chart Comarasion : ")
        st.bar_chart(df)

        # Pie chart with company + price (no percentage)
        fig1, ax1 = plt.subplots(facecolor='none')

        labels = [f"{name}" for name, price in zip(med_name, med_price)]


        def func(pct, allvals):
            absolute = int(round(pct / 100. * sum(allvals)))
            return f"₹{absolute}"  # show price instead of %


        ax1.pie(
            med_price,
            labels=labels,
            startangle=90,
            autopct=lambda pct: func(pct, med_price),  # show ₹price inside
            textprops={'color': "white"}  # text color white (for dark theme)
        )

        ax1.axis('equal')
        fig1.patch.set_alpha(0.0)
        st.pyplot(fig1)

        # ax1.pie(med_price, labels=labels, startangle=90)
        # ax1.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle.
        # st.pyplot(fig1)

# streamlit run app.py