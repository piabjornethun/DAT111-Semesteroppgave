# importing modules and packages
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import matplotlib.image as mpimg
from Semester26_Model import  predict_price

def draw_the_map():
    ax_map.cla()
    ax_map.imshow(img, extent=(0, 100, 0, 100), aspect='auto')
    x,y = marked_point
    ax_map.scatter(x, y, marker='o', c='blue', s=120,
                   edgecolors='white', linewidths=2)
    print(f"marked_point: {marked_point}")
    if marked_point == (0, 0):
        return

    m2_price:float = predict_price(x, y, m2, house_type, standard_type) / m2
    total_price = m2_price * m2 * 1000
    price_box.set_text(f"Estimert boligpris:\n{total_price:,.0f} kr")
    price = f"{round(m2_price * 1000, -2):,.0f}"

    m2list = [50,100,150,200]
    price_m2 = [predict_price(x, y,  _m2, house_type, standard_type)/_m2 for _m2 in m2list]

    ax_map.text(x + 3, y - 1, price, color='blue', fontsize=15)
    ax_history.cla()

    #   Endrer farger på stolper utifra standard:

    colors = {
        1: "red",
        2: "gold",
        3: "limegreen",
        4: "darkgreen"
    }

    ax_history.bar(m2list, price_m2, color=colors[standard_type], width=5, label="Pris per m²")

    reference_value = price_m2[m2list.index(100)]

    ax_history.axhline(y=reference_value, color="black", linestyle="--", linewidth=1.5, alpha=0.8)
    ax_history.text(195, reference_value - 3, "Referanse: 100 m²", fontsize=9, color="seagreen", ha="right", va="top")
    ax_history.set_title("Kvadratmeterpris", fontsize=13, fontweight="bold")
    ax_history.set_xlabel("Boligstørrelse (m²)", fontsize=11)
    ax_history.set_ylabel("Pris per m² (1000 kr)", fontsize=11)
    ax_history.grid(axis="y", linestyle="--", alpha=0.3)
    ax_history.set_axisbelow(True)

    plt.draw()

def on_click_map(event) :
    global marked_point
    if event.inaxes != ax_map:
        return
    marked_point = (event.xdata, event.ydata)
    draw_the_map()
    return

def on_house_type(key):
    global house_type
    house_type = house_types[key]
    draw_the_map()

def on_standard(key):
    global standard_type
    standard_type = standard_types[key]
    draw_the_map()

house_types = {
    'Enebolig': 1,
    'Rekke': 2,
    'Leilighet': 3
}
standard_types = {
    'Dårlig': 1,
    'God': 2,
    'Meget God': 3,
    'Luksus': 4
}

house_type = 1
standard_type = 1
m2 = 100
marked_point = (43,57)

# Create the figures
fig = plt.figure(figsize=(11, 7), facecolor="whitesmoke")
fig.suptitle("Boligpriser i Bergen", fontsize=22, color="#436982", fontweight="bold", y=0.97)

ax_map = fig.add_axes((0.40, 0.07, 0.57, 0.83))
ax_radio_house_type = fig.add_axes((0.05, 0.82, 0.28, 0.10))
ax_radio_standard = fig.add_axes((0.05, 0.63, 0.28, 0.13))
ax_history = fig.add_axes((0.07, 0.07, 0.27, 0.30))
price_box = fig.text(0.06, 0.50,"",fontsize=13,fontweight="bold",color="seagreen",bbox=dict(facecolor="white", edgecolor="lightgray", boxstyle="round,pad=0.6"))
ax_radio_house_type.set_facecolor('white')
ax_radio_standard.set_facecolor('white')
ax_radio_house_type.set_title("Boligtype", fontsize=12, fontweight="bold")
ax_radio_standard.set_title("Standard", fontsize=12, fontweight="bold")

radio_button_category = RadioButtons(ax_radio_house_type, list(house_types.keys()), activecolor="seagreen")
radio_button_standard = RadioButtons(ax_radio_standard, list(standard_types.keys()), activecolor="seagreen")
radio_button_category.on_clicked(on_house_type)
radio_button_standard.on_clicked(on_standard)

fig.subplots_adjust(left=0, right=1, top=1, bottom=0) # Adjust the figure to fit the image
ax_map.margins(x=0.01, y=0.01)  # Adjust x and y margins
img = mpimg.imread('Semester26_Bergen.jpg')
ax_map.imshow(img, aspect='auto')

draw_the_map()

plt.connect('button_press_event', on_click_map)
plt.show()


