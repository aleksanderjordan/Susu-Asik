import streamlit as st, pandas as pd

st.set_page_config(page_title="Susu Asik", layout="wide")
st.markdown("<h1 style='text-align: center;'>Menu Susu Asik 🐮</h1>", unsafe_allow_html=True)

menu_data = {
    "Menu Utama & Rasa Buah": {
        "Susu Original": [6000, "Gambar/Susu Original.jpg"],
        "Susu Cokelat": [8000, "Gambar/Susu Cokelat.jpg"],
        "Susu Stroberi": [8000, "Gambar/Susu Stroberi.jpg"],
        "Susu Melon": [8000, "Gambar/Susu Melon.jpg"],
        "Susu Mangga": [8000, "Gambar/Susu Mangga.jpg"],
        "Susu Banana": [8000, "Gambar/Susu Banana.jpg"],
        "Susu Avocado": [8000, "Gambar/Susu Avocado.jpg"],
        "Susu Bluberi": [8000, "Gambar/Susu Bluberi.jpg"],
        "Susu Anggur": [8000, "Gambar/Susu Anggur.jpg"],
        "Susu Durian": [8000, "Gambar/Susu Durian.jpg"]
    },
    "Menu Coffee, Tea, & Lain-lain": {
        "Susu Coffee": [8000, "Gambar/Susu Coffee.jpg"],
        "Susu Cappucino": [8000, "Gambar/Susu Cappucino.jpg"],
        "Susu Vanila": [8000, "Gambar/Susu Vanila.jpg"],
        "Susu Milktea": [10000, "Gambar/Susu Milktea.jpg"],
        "Susu Bubble Gum": [10000, "Gambar/Susu Bubble Gum.jpg"],
        "Susu Choco Hazelnut": [13000, "Gambar/Susu Choco Hazelnut.jpg"],
        "Susu Milo": [13000, "Gambar/Susu Milo.jpg"],
        "Kopi Matcha": [13000, "Gambar/Susu Matcha.jpg"]
    },
    "Menu Spesial": {
        "Susu Oreo": [10000, "Gambar/Susu Oreo.jpg"],
        "Susu Regal": [10000, "Gambar/Susu Regal.jpg"],
        "Susu Redvelvet": [10000, "Gambar/Susu Redvelvet.jpg"],
        "Susu Taro": [10000, "Gambar/Susu Taro.jpg"],
        "Susu Pink Lava": [10000, "Gambar/Susu Pink Lava.jpg"]
    },
    "Roti Bakar": {
        "Rotbar Stroberi": [8000, "Gambar/Rotbar Stroberi.jpg"],
        "Rotbar Bluberi": [8000, "Gambar/Rotbar Bluberi.jpg"],
        "Rotbar Nanas": [8000, "Gambar/Rotbar Nanas.jpg"],
        "Rotbar Meses": [10000, "Gambar/Rotbar Meses.png"],
        "Rotbar Keju": [12000, "Gambar/Rotbar Keju.jpg"],
        "Rotbar Tiramisu": [12000, "Gambar/Rotbar Tiramisu.jpg"],
        "Rotbar Greentea": [12000, "Gambar/Rotbar Greentea.jpg"],
        "Rotbar Choco Crunchy": [12000, "Gambar/Rotbar Choco Crunchy.jpg"],
        "Rotbar Choco Crunchy Keju": [15000, "Gambar/Rotbar Choco Crunchy Keju.png"],
    }
}

if "order_items" not in st.session_state:
    st.session_state.order_items = []

if "selected_category" not in st.session_state:
    st.session_state.selected_category = list(menu_data.keys())[0]

if "last_added_key" not in st.session_state:
    st.session_state.last_added_key = None

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
cols = st.columns(5)

def reset_input_for(menu):
    for key in list(st.session_state.keys()):
        if key.startswith(f"qty_{menu}") or \
           key.startswith(f"ukuran_{menu}") or \
           key.startswith(f"porsi_{menu}") or \
           key.startswith(f"rasa_{menu}") or \
           key.startswith(f"topping_{menu}"):
            del st.session_state[key]

for i, menu in enumerate(menu_names):
    with cols[i % 5]:
        harga_dasar = selected_data[menu][0]
        st.image(selected_data[menu][1], use_container_width=True)
        st.markdown(
            f"""
            <div style='font-weight:bold; font-size:16px; color:white; text-align:center; margin-top:4px;'>
                {menu}
            </div>
            """, unsafe_allow_html=True
        )

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
                                harga_tambahan = selected_data[r][0]
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
