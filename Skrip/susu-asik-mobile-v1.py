import streamlit as st, pandas as pd

st.set_page_config(page_title="Susu Asik", layout="wide")
st.markdown("<h1 style='text-align: center;'>Menu Susu Asik 🐮</h1>", unsafe_allow_html=True)

st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    font-size: 22px;
    font-weight: 900;
    padding: 14px;
    margin-bottom: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

menu_data = {
    "Menu Utama & Rasa Buah": {
        "Susu Original": 6000,
        "Susu Cokelat": 8000,
        "Susu Stroberi": 8000,
        "Susu Melon": 8000,
        "Susu Mangga": 8000,
        "Susu Banana": 8000,
        "Susu Avocado": 8000,
        "Susu Bluberi": 8000,
        "Susu Anggur": 8000,
        "Susu Durian": 8000
    },
    "Menu Coffee, Tea, & Lain-lain": {
        "Susu Coffee": 8000,
        "Susu Cappucino": 8000,
        "Susu Vanila": 8000,
        "Susu Milktea": 10000,
        "Susu Bubble Gum": 10000,
        "Susu Choco Hazelnut": 13000,
        "Susu Milo": 13000,
        "Kopi Matcha": 13000
    },
    "Menu Spesial": {
        "Susu Oreo": 10000,
        "Susu Regal": 10000,
        "Susu Redvelvet": 10000,
        "Susu Taro": 10000,
        "Susu Pink Lava": 10000
    },
    "Roti Bakar": {
        "Rotbar Stroberi": 8000,
        "Rotbar Bluberi": 8000,
        "Rotbar Nanas": 8000,
        "Rotbar Meses": 10000,
        "Rotbar Keju": 12000,
        "Rotbar Tiramisu": 12000,
        "Rotbar Greentea": 12000,
        "Rotbar Choco Crunchy": 12000,
        "Rotbar Choco Crunchy Keju": 15000
    }
}

if "order_items" not in st.session_state:
    st.session_state.order_items = []

if "selected_category" not in st.session_state:
    st.session_state.selected_category = list(menu_data.keys())[0]

if "last_added_key" not in st.session_state:
    st.session_state.last_added_key = None

if "active_menu" not in st.session_state:
    st.session_state.active_menu = None

selected_radio = st.radio(
    "Pilih Kategori Menu:",
    options=list(menu_data.keys()),
    index=list(menu_data.keys()).index(st.session_state.selected_category),
    horizontal=True,
    key="selected_category_radio"
)

if selected_radio != st.session_state.selected_category:
    st.session_state.selected_category = selected_radio
    st.rerun()

selected_category = st.session_state.selected_category
selected_data = menu_data[selected_category]
menu_names = list(selected_data.keys())

def reset_input_for(menu):
    for key in list(st.session_state.keys()):
        if key.startswith(f"qty_{menu}") or \
           key.startswith(f"ukuran_{menu}") or \
           key.startswith(f"porsi_{menu}") or \
           key.startswith(f"rasa_{menu}") or \
           key.startswith(f"topping_{menu}"):
            del st.session_state[key]

for i, menu in enumerate(menu_names):
    if st.button(menu, key=f"btn_{menu}"):
        st.session_state.active_menu = menu if st.session_state.active_menu != menu else None
        st.rerun()

    if st.session_state.active_menu == menu:
        with st.container():
            harga_dasar = selected_data[menu]

            qty = st.number_input("Jumlah", min_value=0, step=1,
                                  value=st.session_state.get(f"qty_{menu}", 0),
                                  key=f"qty_{menu}")

            if selected_category == "Roti Bakar":
                porsi_default = st.session_state.get(f"porsi_{menu}", "Porsi Pas")
                porsi = st.selectbox("Porsi", ["Porsi Pas", "Porsi Puas"],
                                     index=["Porsi Pas", "Porsi Puas"].index(porsi_default),
                                     key=f"porsi_{menu}")

                rasa_list = ["Tidak"] + [r.replace("Rotbar ", "") for r in selected_data if r != menu]
                rasa_default = st.session_state.get(f"rasa_{menu}", "Tidak")
                rasa_tambahan = st.selectbox("Rasa tambahan (opsional)", rasa_list,
                                             index=rasa_list.index(rasa_default),
                                             key=f"rasa_{menu}")

                button_key = f"add_{menu}_{porsi}_{rasa_tambahan}"
                if qty > 0 and st.button(f"Tambah {menu}", key=button_key):
                    if st.session_state.last_added_key != button_key:
                        st.session_state.last_added_key = button_key
                        harga = harga_dasar
                        if rasa_tambahan != "Tidak":
                            for r in selected_data:
                                if r.replace("Rotbar ", "") == rasa_tambahan:
                                    harga_tambahan = selected_data[r]
                                    break
                            else:
                                harga_tambahan = 0
                            harga = max(harga_dasar, harga_tambahan) if porsi == "Porsi Pas" else harga_dasar + harga_tambahan
                            rasa_final = f"{menu}, {rasa_tambahan}"
                        else:
                            if porsi == "Porsi Puas":
                                harga = harga_dasar * 2
                            rasa_final = menu

                        st.session_state.order_items.append({
                            "Menu": menu,
                            "Ukuran/Porsi": porsi,
                            "Topping/Rasa Tambahan": rasa_final,
                            "Jumlah": qty,
                            "Harga Satuan": harga,
                            "Total": harga * qty
                        })
                        reset_input_for(menu)
                        st.session_state.active_menu = None
                        st.rerun()
            else:
                ukuran_default = st.session_state.get(f"ukuran_{menu}", "Medium")
                ukuran = st.selectbox("Ukuran", ["Medium", "Large", "Hangat"],
                                      index=["Medium", "Large", "Hangat"].index(ukuran_default),
                                      key=f"ukuran_{menu}")

                topping_default = st.session_state.get(f"topping_{menu}", [])
                topping = st.multiselect("Topping", ["Oreo", "Regal"],
                                         default=topping_default,
                                         key=f"topping_{menu}")
                topping_str = ",".join(sorted(topping))

                button_key = f"add_{menu}_{ukuran}_{topping_str}"
                if qty > 0 and st.button(f"Tambah {menu}", key=button_key):
                    if st.session_state.last_added_key != button_key:
                        st.session_state.last_added_key = button_key
                        harga = harga_dasar + (2000 if ukuran == "Large" else 0) + 2000 * len(topping)
                        st.session_state.order_items.append({
                            "Menu": menu,
                            "Ukuran/Porsi": ukuran,
                            "Topping/Rasa Tambahan": topping_str,
                            "Jumlah": qty,
                            "Harga Satuan": harga,
                            "Total": harga * qty
                        })
                        reset_input_for(menu)
                        st.session_state.active_menu = None
                        st.rerun()

if st.session_state.order_items:
    df = pd.DataFrame(st.session_state.order_items)
    total_harga = df["Total"].sum()

    st.markdown("### Ringkasan Pesanan")
    st.dataframe(df, use_container_width=True)
    st.success(f"Total Harga: Rp{total_harga:,}")

    def reset_all_inputs():
        st.session_state.order_items = []
        st.session_state.last_added_key = None
        for key in list(st.session_state.keys()):
            if key.startswith(("qty_", "ukuran_", "porsi_", "rasa_", "topping_")):
                del st.session_state[key]

    if st.button("Reset Pesanan", type="secondary"):
        reset_all_inputs()
        st.rerun()
else:
    st.info("Silakan pilih menu dan klik 'Tambah' untuk membuat pesanan.")